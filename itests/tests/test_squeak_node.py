from __future__ import print_function

import datetime
import time

import pytest
from squeak.core import CheckSqueak
from squeak.core import CSqueak

from proto import lnd_pb2 as ln
from proto import squeak_admin_pb2
from tests.util import connect_peer
from tests.util import create_saved_peer
from tests.util import download_offers
from tests.util import download_squeak
from tests.util import get_connected_peer
from tests.util import get_connected_peers
from tests.util import get_hash
from tests.util import get_squeak_display
from tests.util import get_squeak_profile
from tests.util import open_channel
from tests.util import open_peer_connection
from tests.util import subscribe_connected_peers


def test_get_network(admin_stub):
    # Get the network
    get_network_response = admin_stub.GetNetwork(
        squeak_admin_pb2.GetNetworkRequest()
    )
    network = get_network_response.network

    assert network == "simnet"


def test_reprocess_received_payments(admin_stub):
    # Reprocess received payments
    reprocess_received_payments_response = admin_stub.ReprocessReceivedPayments(
        squeak_admin_pb2.ReprocessReceivedPaymentsRequest()
    )

    assert reprocess_received_payments_response is not None


def test_get_profile(admin_stub, signing_profile_id):
    # Get the squeak profile
    squeak_profile = get_squeak_profile(admin_stub, signing_profile_id)
    address = squeak_profile.address
    name = squeak_profile.profile_name

    # Get the same squeak profile by address
    get_squeak_profile_by_address_response = admin_stub.GetSqueakProfileByAddress(
        squeak_admin_pb2.GetSqueakProfileByAddressRequest(
            address=address,
        )
    )
    assert address == get_squeak_profile_by_address_response.squeak_profile.address
    assert name == get_squeak_profile_by_address_response.squeak_profile.profile_name

    # Get the same squeak profile by name
    get_squeak_profile_by_name_response = admin_stub.GetSqueakProfileByName(
        squeak_admin_pb2.GetSqueakProfileByNameRequest(
            name=name,
        )
    )
    assert address == get_squeak_profile_by_name_response.squeak_profile.address
    assert name == get_squeak_profile_by_name_response.squeak_profile.profile_name


def test_make_squeak(admin_stub, signing_profile_id):
    # Create a new squeak using the new profile
    make_squeak_content = "Hello from the profile on the server!"
    make_squeak_response = admin_stub.MakeSqueak(
        squeak_admin_pb2.MakeSqueakRequest(
            profile_id=signing_profile_id,
            content=make_squeak_content,
        )
    )
    make_squeak_hash = make_squeak_response.squeak_hash
    assert len(make_squeak_hash) == 32 * 2

    # Get the squeak display item
    get_squeak_display_response = admin_stub.GetSqueakDisplay(
        squeak_admin_pb2.GetSqueakDisplayRequest(
            squeak_hash=make_squeak_hash,
        )
    )
    assert get_squeak_display_response.squeak_display_entry.squeak_hash == make_squeak_hash
    assert (
        get_squeak_display_response.squeak_display_entry.content_str == "Hello from the profile on the server!"
    )
    # assert get_squeak_display_response.squeak_display_entry.author_address == signing_profile_address
    assert get_squeak_display_response.squeak_display_entry.is_author_known
    assert get_squeak_display_response.squeak_display_entry.HasField("author")
    assert len(
        get_squeak_display_response.squeak_display_entry.author.profile_image) > 0

    # Get the squeak profile
    squeak_profile = get_squeak_profile(admin_stub, signing_profile_id)
    squeak_profile_address = squeak_profile.address
    squeak_profile_name = squeak_profile.profile_name

    # Get all squeak displays for the known address
    get_address_squeak_display_response = admin_stub.GetAddressSqueakDisplays(
        squeak_admin_pb2.GetAddressSqueakDisplaysRequest(
            address=squeak_profile_address)
    )
    assert len(get_address_squeak_display_response.squeak_display_entries) == 1
    for (
        squeak_display_entry
    ) in get_address_squeak_display_response.squeak_display_entries:
        assert squeak_display_entry.author.profile_name == squeak_profile_name
        assert squeak_display_entry.author.address == squeak_profile_address


def test_make_reply_squeak(
    admin_stub, saved_squeak_hash, signing_profile_id
):
    # Make another squeak as a reply
    reply_1_squeak_response = admin_stub.MakeSqueak(
        squeak_admin_pb2.MakeSqueakRequest(
            profile_id=signing_profile_id,
            content="Reply #1",
            replyto=saved_squeak_hash,
        )
    )
    reply_1_squeak_hash = reply_1_squeak_response.squeak_hash

    # Make a second squeak as a reply
    reply_2_squeak_response = admin_stub.MakeSqueak(
        squeak_admin_pb2.MakeSqueakRequest(
            profile_id=signing_profile_id,
            content="Reply #2",
            replyto=reply_1_squeak_hash,
        )
    )
    reply_2_squeak_hash = reply_2_squeak_response.squeak_hash

    # Get the squeak and check that the reply field is correct
    get_reply_squeak_display_response = admin_stub.GetSqueakDisplay(
        squeak_admin_pb2.GetSqueakDisplayRequest(
            squeak_hash=reply_2_squeak_hash,
        )
    )
    assert (
        get_reply_squeak_display_response.squeak_display_entry.squeak_hash == reply_2_squeak_hash
    )
    assert (
        get_reply_squeak_display_response.squeak_display_entry.reply_to == reply_1_squeak_hash
    )

    # Get the ancestors of the latest reply squeak
    get_ancestors_response = admin_stub.GetAncestorSqueakDisplays(
        squeak_admin_pb2.GetAncestorSqueakDisplaysRequest(
            squeak_hash=reply_2_squeak_hash,
        )
    )
    assert len(get_ancestors_response.squeak_display_entries) == 3

    # Get the replies of the original squeak
    get_replies_response = admin_stub.GetReplySqueakDisplays(
        squeak_admin_pb2.GetReplySqueakDisplaysRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    assert len(get_replies_response.squeak_display_entries) == 1
    assert reply_1_squeak_hash in [
        entry.squeak_hash
        for entry in get_replies_response.squeak_display_entries
    ]


def test_make_signing_profile(admin_stub):
    # Create a new signing profile
    profile_name = "test_signing_profile_name"
    create_signing_profile_response = admin_stub.CreateSigningProfile(
        squeak_admin_pb2.CreateSigningProfileRequest(
            profile_name=profile_name,
        )
    )
    profile_id = create_signing_profile_response.profile_id

    # Get the new squeak profile
    squeak_profile = get_squeak_profile(admin_stub, profile_id)
    assert squeak_profile.profile_name == profile_name
    squeak_profile_address = squeak_profile.address

    # Get all signing profiles
    get_signing_profiles_response = admin_stub.GetSigningProfiles(
        squeak_admin_pb2.GetSigningProfilesRequest()
    )
    signing_profile_names = [
        profile.profile_name
        for profile in get_signing_profiles_response.squeak_profiles
    ]
    assert profile_name in signing_profile_names

    # Get squeak profile by address
    get_profile_by_address_response = admin_stub.GetSqueakProfileByAddress(
        squeak_admin_pb2.GetSqueakProfileByAddressRequest(
            address=squeak_profile_address
        )
    )
    assert get_profile_by_address_response.squeak_profile.profile_name == profile_name

    # Export the private key, delete the profile, and re-import it.
    get_private_key_response = admin_stub.GetSqueakProfilePrivateKey(
        squeak_admin_pb2.GetSqueakProfilePrivateKeyRequest(
            profile_id=profile_id,
        )
    )
    private_key = get_private_key_response.private_key
    admin_stub.DeleteSqueakProfile(
        squeak_admin_pb2.DeleteSqueakProfileRequest(
            profile_id=profile_id,
        )
    )
    import_response = admin_stub.ImportSigningProfile(
        squeak_admin_pb2.ImportSigningProfileRequest(
            profile_name="imported_profile_name",
            private_key=private_key,
        )
    )
    new_profile_id = import_response.profile_id

    # Get the new imported profile
    squeak_profile = get_squeak_profile(admin_stub, new_profile_id)
    assert squeak_profile.profile_name == "imported_profile_name"
    assert squeak_profile.address == squeak_profile_address


def test_make_contact_profile(admin_stub, squeak_address):
    # Create a new contact profile
    contact_name = "test_contact_profile_name"
    create_contact_profile_response = admin_stub.CreateContactProfile(
        squeak_admin_pb2.CreateContactProfileRequest(
            profile_name=contact_name,
            address=squeak_address,
        )
    )
    contact_profile_id = create_contact_profile_response.profile_id

    # Get all contact profiles
    get_contact_profiles_response = admin_stub.GetContactProfiles(
        squeak_admin_pb2.GetContactProfilesRequest()
    )
    contact_profile_names = [
        profile.profile_name
        for profile in get_contact_profiles_response.squeak_profiles
    ]
    contact_profile_ids = [
        profile.profile_id
        for profile in get_contact_profiles_response.squeak_profiles
    ]
    assert contact_name in contact_profile_names
    assert contact_profile_id in contact_profile_ids


def test_make_signing_profile_empty_name(admin_stub):
    # Try to create a new signing profile with an empty name
    with pytest.raises(Exception) as excinfo:
        admin_stub.CreateSigningProfile(
            squeak_admin_pb2.CreateSigningProfileRequest(
                profile_name="",
            )
        )
    assert "Profile name cannot be empty." in str(excinfo.value)


def test_make_contact_profile_empty_name(admin_stub, squeak_address):
    # Try to create a new contact profile with an empty name
    with pytest.raises(Exception) as excinfo:
        admin_stub.CreateContactProfile(
            squeak_admin_pb2.CreateContactProfileRequest(
                profile_name="",
                address=squeak_address,
            )
        )
    assert "Profile name cannot be empty." in str(excinfo.value)


def test_set_profile_following(admin_stub, contact_profile_id):
    # Set the profile to be following
    admin_stub.SetSqueakProfileFollowing(
        squeak_admin_pb2.SetSqueakProfileFollowingRequest(
            profile_id=contact_profile_id,
            following=True,
        )
    )

    # Get the squeak profile again
    squeak_profile = get_squeak_profile(admin_stub, contact_profile_id)
    assert squeak_profile.following

    # Set the profile to be not following
    admin_stub.SetSqueakProfileFollowing(
        squeak_admin_pb2.SetSqueakProfileFollowingRequest(
            profile_id=contact_profile_id,
            following=False,
        )
    )

    # Get the squeak profile again
    squeak_profile = get_squeak_profile(admin_stub, contact_profile_id)
    assert not squeak_profile.following


def test_rename_profile(admin_stub, contact_profile_id, random_name):
    # Rename the profile to something new
    admin_stub.RenameSqueakProfile(
        squeak_admin_pb2.RenameSqueakProfileRequest(
            profile_id=contact_profile_id,
            profile_name=random_name,
        )
    )

    # Get the squeak profile
    squeak_profile = get_squeak_profile(admin_stub, contact_profile_id)
    assert squeak_profile.profile_name == random_name


def test_set_profile_image(admin_stub, contact_profile_id, random_image, random_image_base64_string):
    # print("random_image: {}".format(random_image))
    # print("random_image_base64_string: {}".format(random_image_base64_string))
    # Set the profile image to something new
    admin_stub.SetSqueakProfileImage(
        squeak_admin_pb2.SetSqueakProfileImageRequest(
            profile_id=contact_profile_id,
            profile_image=random_image_base64_string,
        )
    )

    # Get the squeak profile
    squeak_profile = get_squeak_profile(admin_stub, contact_profile_id)
    assert squeak_profile.profile_image == random_image_base64_string
    assert squeak_profile.has_custom_profile_image

    # Clear the profile image
    admin_stub.ClearSqueakProfileImage(
        squeak_admin_pb2.ClearSqueakProfileImageRequest(
            profile_id=contact_profile_id,
        )
    )

    # Get the squeak profile
    squeak_profile = get_squeak_profile(admin_stub, contact_profile_id)
    assert squeak_profile.profile_image != random_image_base64_string
    assert not squeak_profile.has_custom_profile_image


def test_delete_profile(admin_stub, random_name, squeak_address, contact_profile_id):
    # Delete the profile
    admin_stub.DeleteSqueakProfile(
        squeak_admin_pb2.DeleteSqueakProfileRequest(
            profile_id=contact_profile_id,
        )
    )

    # Try to get the profile and fail
    squeak_profile = get_squeak_profile(admin_stub, contact_profile_id)
    assert squeak_profile is None

    get_squeak_profile_by_name_response = admin_stub.GetSqueakProfileByName(
        squeak_admin_pb2.GetSqueakProfileByNameRequest(
            name=random_name,
        )
    )
    assert not get_squeak_profile_by_name_response.HasField("squeak_profile")

    get_squeak_profile_by_address_response = admin_stub.GetSqueakProfileByAddress(
        squeak_admin_pb2.GetSqueakProfileByAddressRequest(
            address=squeak_address,
        )
    )
    assert not get_squeak_profile_by_address_response.HasField(
        "squeak_profile")


def test_get_profile_private_key(admin_stub, signing_profile_id):
    # Get the private key
    private_key_response = admin_stub.GetSqueakProfilePrivateKey(
        squeak_admin_pb2.GetSqueakProfilePrivateKeyRequest(
            profile_id=signing_profile_id,
        )
    )

    # print(private_key_response.private_key)
    assert len(private_key_response.private_key) > 0


def test_get_following_squeaks(
    admin_stub, saved_squeak_hash, signing_profile_id
):
    # Set the profile to be following
    admin_stub.SetSqueakProfileFollowing(
        squeak_admin_pb2.SetSqueakProfileFollowingRequest(
            profile_id=signing_profile_id,
            following=True,
        )
    )

    # Get all squeak displays for the known address
    get_timeline_squeak_display_response = admin_stub.GetTimelineSqueakDisplays(
        squeak_admin_pb2.GetTimelineSqueakDisplaysRequest()
    )
    assert len(get_timeline_squeak_display_response.squeak_display_entries) >= 1
    for (
        squeak_display_entry
    ) in get_timeline_squeak_display_response.squeak_display_entries:
        # TODO: check the profile id of the squeak display entry
        # assert squeak_display_entry.profile_id == signing_profile_id
        pass


def test_delete_squeak(admin_stub, saved_squeak_hash):
    # Delete the squeak
    admin_stub.DeleteSqueak(
        squeak_admin_pb2.DeleteSqueakRequest(squeak_hash=saved_squeak_hash)
    )

    # Try to get the squeak display item
    get_squeak_display_response = admin_stub.GetSqueakDisplay(
        squeak_admin_pb2.GetSqueakDisplayRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    print("-----------------------------")
    print("get_squeak_display_response:")
    print(get_squeak_display_response)
    print(dir(get_squeak_display_response))
    print("-----------------------------")
    print("get_squeak_display_response.squeak_display_entry:")
    print((get_squeak_display_response.squeak_display_entry))
    assert not get_squeak_display_response.HasField("squeak_display_entry")


def test_create_peer(admin_stub):
    # Add a new peer
    peer_id = create_saved_peer(
        admin_stub,
        "fake_peer_name",
        "fake_host",
        1234,
    )

    # Get the new peer
    get_peer_response = admin_stub.GetPeer(
        squeak_admin_pb2.GetPeerRequest(
            peer_id=peer_id,
        )
    )
    assert get_peer_response.squeak_peer.peer_address.host == "fake_host"
    assert get_peer_response.squeak_peer.peer_address.port == 1234

    # Get all peers
    get_peers_response = admin_stub.GetPeers(
        squeak_admin_pb2.GetPeersRequest())
    peer_hosts = [
        squeak_peer.peer_address.host
        for squeak_peer in get_peers_response.squeak_peers
    ]
    assert "fake_host" in peer_hosts


def test_create_peer_empty_name(admin_stub):
    # Try to create a new signing profile with an empty name
    with pytest.raises(Exception) as excinfo:
        create_saved_peer(
            admin_stub,
            "",
            "another_fake_host",
            1234,
        )
    assert "Peer name cannot be empty." in str(excinfo.value)


def test_set_peer_autoconnect(admin_stub, peer_id):
    # Get the peer
    get_peer_response = admin_stub.GetPeer(
        squeak_admin_pb2.GetPeerRequest(
            peer_id=peer_id,
        )
    )
    assert not get_peer_response.squeak_peer.autoconnect

    # Set the peer to be autoconnect
    admin_stub.SetPeerAutoconnect(
        squeak_admin_pb2.SetPeerAutoconnectRequest(
            peer_id=peer_id,
            autoconnect=True,
        )
    )

    # Get the peer again
    get_peer_response = admin_stub.GetPeer(
        squeak_admin_pb2.GetPeerRequest(
            peer_id=peer_id,
        )
    )
    assert get_peer_response.squeak_peer.autoconnect


def test_rename_peer(admin_stub, peer_id, random_name):
    # Rename the peer
    admin_stub.RenamePeer(
        squeak_admin_pb2.RenamePeerRequest(
            peer_id=peer_id,
            peer_name=random_name,
        )
    )

    # Get the peer again
    get_peer_response = admin_stub.GetPeer(
        squeak_admin_pb2.GetPeerRequest(
            peer_id=peer_id,
        )
    )
    assert get_peer_response.squeak_peer.peer_name == random_name


def test_delete_peer(admin_stub, peer_id):
    # Delete the peer
    admin_stub.DeletePeer(
        squeak_admin_pb2.DeletePeerRequest(
            peer_id=peer_id,
        )
    )

    get_peer_response = admin_stub.GetPeer(
        squeak_admin_pb2.GetPeerRequest(
            peer_id=peer_id,
        )
    )
    assert not get_peer_response.HasField("squeak_peer")


def test_send_coins(admin_stub, lightning_client):
    new_address_response = admin_stub.LndNewAddress(ln.NewAddressRequest())
    send_coins_response = lightning_client.send_coins(
        new_address_response.address, 55555555
    )
    time.sleep(10)
    get_transactions_response = admin_stub.LndGetTransactions(
        ln.GetTransactionsRequest()
    )

    assert any(
        [
            transaction.tx_hash == send_coins_response.txid
            for transaction in get_transactions_response.transactions
        ]
    )


def test_buy_squeak(
    admin_stub,
    other_admin_stub,
    connected_tcp_peer_id,
    lightning_client,
    signing_profile_id,
    saved_squeak_hash,
):
    # Download squeak
    download_squeak(other_admin_stub, saved_squeak_hash)
    time.sleep(5)

    # Download offer
    download_offers(other_admin_stub, saved_squeak_hash)
    time.sleep(5)

    # Get the sent offers from the seller node
    get_sent_offers_response = admin_stub.GetSentOffers(
        squeak_admin_pb2.GetSentOffersRequest(),
    )
    squeak_hashes = [
        sent_offer.squeak_hash
        for sent_offer in get_sent_offers_response.sent_offers
    ]
    assert saved_squeak_hash in squeak_hashes

    # Get the buy offer
    get_buy_offers_response = other_admin_stub.GetBuyOffers(
        squeak_admin_pb2.GetBuyOffersRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    # print(get_buy_offers_response)
    assert len(get_buy_offers_response.offers) > 0

    offer = get_buy_offers_response.offers[0]

    with connect_peer(
        lightning_client, offer.node_host, offer.node_pubkey
    ), open_channel(lightning_client, offer.node_pubkey, 1000000):

        lightning_client.list_channels()
        # print(list_channels_response)

        # Pay the offer
        pay_offer_response = other_admin_stub.PayOffer(
            squeak_admin_pb2.PayOfferRequest(
                offer_id=offer.offer_id,
            )
        )
        # print(pay_offer_response)
        assert pay_offer_response.sent_payment_id > 0

        # Get the squeak display item
        get_squeak_display_response = other_admin_stub.GetSqueakDisplay(
            squeak_admin_pb2.GetSqueakDisplayRequest(
                squeak_hash=saved_squeak_hash,
            )
        )
        assert (
            get_squeak_display_response.squeak_display_entry.content_str == "Hello from the profile on the server!"
        )

        # Get all sent payments
        get_sent_payments_response = other_admin_stub.GetSentPayments(
            squeak_admin_pb2.GetSentPaymentsRequest(),
        )
        squeak_hashes = [
            sent_payment.squeak_hash
            for sent_payment in get_sent_payments_response.sent_payments
        ]
        assert saved_squeak_hash in squeak_hashes

        # Get the single sent payment
        for sent_payment in get_sent_payments_response.sent_payments:
            if sent_payment.squeak_hash == saved_squeak_hash:
                sent_payment_id = sent_payment.sent_payment_id
        get_sent_payment_response = other_admin_stub.GetSentPayment(
            squeak_admin_pb2.GetSentPaymentRequest(
                sent_payment_id=sent_payment_id,
            ),
        )
        assert saved_squeak_hash == get_sent_payment_response.sent_payment.squeak_hash
        assert get_sent_payment_response.sent_payment.price_msat == 1000000
        assert get_sent_payment_response.sent_payment.valid

        # Get the received payment from the seller node
        get_received_payments_response = admin_stub.GetReceivedPayments(
            squeak_admin_pb2.GetReceivedPaymentsRequest(),
        )
        # print(
        #     "get_received_payments_response: {}".format(
        #         get_received_payments_response)
        # )
        payment_hashes = [
            received_payment.payment_hash
            for received_payment in get_received_payments_response.received_payments
        ]
        assert sent_payment.payment_hash in payment_hashes
        for received_payment in get_received_payments_response.received_payments:
            received_payment_time_s = received_payment.time_s
            # print("received_payment_time_s: {}".format(
            #     received_payment_time_s))
            received_payment_time = datetime.datetime.fromtimestamp(
                received_payment_time_s
            )
            five_minutes = datetime.timedelta(minutes=5)
            assert received_payment_time > datetime.datetime.now() - five_minutes
            assert received_payment_time < datetime.datetime.now()
            assert len(received_payment.peer_address.host) > 4

        # Subscribe to received payments starting from index zero
        subscribe_received_payments_response = admin_stub.SubscribeReceivedPayments(
            squeak_admin_pb2.SubscribeReceivedPaymentsRequest(
                payment_index=0,
            ),
        )
        for payment in subscribe_received_payments_response:
            # print("Got payment from subscription: {}".format(payment))
            assert payment.received_payment_id == 1
            break

        # Get the payment summary from the seller node
        get_payment_summary_response = admin_stub.GetPaymentSummary(
            squeak_admin_pb2.GetPaymentSummaryRequest(),
        )
        # print(
        #     "get_payment_summary_response from seller: {}".format(
        #         get_payment_summary_response)
        # )
        assert get_payment_summary_response.payment_summary.num_received_payments > 0
        assert get_payment_summary_response.payment_summary.amount_earned_msat > 0

        # Get the payment summary from the buyer node
        get_payment_summary_response = other_admin_stub.GetPaymentSummary(
            squeak_admin_pb2.GetPaymentSummaryRequest(),
        )
        # print(
        #     "get_payment_summary_response from buyer: {}".format(
        #         get_payment_summary_response)
        # )
        assert get_payment_summary_response.payment_summary.num_sent_payments > 0
        assert get_payment_summary_response.payment_summary.amount_spent_msat > 0


def test_download_single_squeak(
    admin_stub,
    other_admin_stub,
    connected_tcp_peer_id,
    lightning_client,
    signing_profile_id,
    saved_squeak_hash,
):
    # Get the squeak display item (should be empty)
    squeak_display_entry = get_squeak_display(
        other_admin_stub, saved_squeak_hash)
    assert squeak_display_entry is None

    # Get buy offers for the squeak hash (should be empty)
    get_buy_offers_response = other_admin_stub.GetBuyOffers(
        squeak_admin_pb2.GetBuyOffersRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    # print(get_buy_offers_response)
    assert len(get_buy_offers_response.offers) == 0

    # Download squeak
    download_squeak(other_admin_stub, saved_squeak_hash)
    time.sleep(5)

    # Get the squeak display item
    squeak_display_entry = get_squeak_display(
        other_admin_stub, saved_squeak_hash)
    assert squeak_display_entry is not None

    # Download offer
    download_offers(other_admin_stub, saved_squeak_hash)
    time.sleep(5)

    # Get the buy offer
    get_buy_offers_response = other_admin_stub.GetBuyOffers(
        squeak_admin_pb2.GetBuyOffersRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    # print(get_buy_offers_response)
    assert len(get_buy_offers_response.offers) > 0


def test_get_squeak_details(admin_stub, saved_squeak_hash):
    # Get the squeak details
    get_squeak_details_response = admin_stub.GetSqueakDetails(
        squeak_admin_pb2.GetSqueakDetailsRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    serialized_squeak_hex = (
        get_squeak_details_response.squeak_detail_entry.serialized_squeak_hex
    )
    # print("serialized_squeak_hex: {}".format(serialized_squeak_hex))
    assert len(serialized_squeak_hex) > 200

    serialized_squeak = bytes.fromhex(serialized_squeak_hex)
    deserialized_squeak = CSqueak.deserialize(serialized_squeak)
    assert get_hash(deserialized_squeak) == saved_squeak_hash
    CheckSqueak(deserialized_squeak)


def test_like_squeak(admin_stub, saved_squeak_hash):
    # Get the squeak display item
    get_squeak_display_response = admin_stub.GetSqueakDisplay(
        squeak_admin_pb2.GetSqueakDisplayRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    # print("get_squeak_display_response.squeak_display_entry:")
    # print(get_squeak_display_response.squeak_display_entry)
    assert (
        get_squeak_display_response.squeak_display_entry.liked_time_s == 0
    )

    # Like the squeak
    admin_stub.LikeSqueak(
        squeak_admin_pb2.LikeSqueakRequest(
            squeak_hash=saved_squeak_hash,
        )
    )

    # Get the squeak display item
    get_squeak_display_response = admin_stub.GetSqueakDisplay(
        squeak_admin_pb2.GetSqueakDisplayRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    assert (
        get_squeak_display_response.squeak_display_entry.liked_time_s > 0
    )

    # Unlike the squeak
    admin_stub.UnlikeSqueak(
        squeak_admin_pb2.UnlikeSqueakRequest(
            squeak_hash=saved_squeak_hash,
        )
    )

    # Get the squeak display item
    get_squeak_display_response = admin_stub.GetSqueakDisplay(
        squeak_admin_pb2.GetSqueakDisplayRequest(
            squeak_hash=saved_squeak_hash,
        )
    )
    assert (
        get_squeak_display_response.squeak_display_entry.liked_time_s == 0
    )


def test_connect_peer(admin_stub, other_admin_stub):
    # connected_peers = get_connected_peers(admin_stub)
    # assert len(connected_peers) == 0
    # other_connected_peers = get_connected_peers(other_admin_stub)
    # assert len(other_connected_peers) == 0

    with subscribe_connected_peers(other_admin_stub) as subscription_queue:
        with open_peer_connection(
                other_admin_stub,
                "test_peer",
                "squeaknode",
                18777,
        ):
            time.sleep(2)
            connected_peers = get_connected_peers(admin_stub)
            print(connected_peers)
            assert len(connected_peers) == 1
            # print("Admin node connected to peers: ")
            # print(connected_peers)
            other_connected_peers = get_connected_peers(other_admin_stub)
            assert len(other_connected_peers) == 1
            # print("Other Admin node connected to peers: ")
            # print(other_connected_peers)
            connected_peer = get_connected_peer(
                other_admin_stub, "squeaknode", 18777)
            assert connected_peer is not None

            # Get item from queue
            item = subscription_queue.get()
            print("item:")
            print(item)
            assert len(item) == 1

        time.sleep(2)
        connected_peers = get_connected_peers(admin_stub)
        assert len(connected_peers) == 0
        other_connected_peers = get_connected_peers(other_admin_stub)
        assert len(other_connected_peers) == 0

        # Get item from queue
        item = subscription_queue.get()
        print("item:")
        print(item)
        assert len(item) == 0


def test_get_squeak_by_lookup(
    admin_stub,
    other_admin_stub,
    connected_tcp_peer_id,
    lightning_client,
    signing_profile_id,
    saved_squeak_hash,
):
    # Get the squeak profile
    squeak_profile = get_squeak_profile(admin_stub, signing_profile_id)
    squeak_profile_address = squeak_profile.address
    squeak_profile_name = squeak_profile.profile_name

    # Add the contact profile to the other server and set the profile to be following
    create_contact_profile_response = other_admin_stub.CreateContactProfile(
        squeak_admin_pb2.CreateContactProfileRequest(
            profile_name=squeak_profile_name,
            address=squeak_profile_address,
        )
    )
    contact_profile_id = create_contact_profile_response.profile_id
    other_admin_stub.SetSqueakProfileFollowing(
        squeak_admin_pb2.SetSqueakProfileFollowingRequest(
            profile_id=contact_profile_id,
            following=True,
        )
    )

    # Get the squeak display item
    squeak_display_entry = get_squeak_display(
        other_admin_stub, saved_squeak_hash)
    print("squeak_display_entry:")
    print(squeak_display_entry)
    assert squeak_display_entry is None

    # Sync squeaks
    other_admin_stub.SyncSqueaks(
        squeak_admin_pb2.SyncSqueaksRequest(),
    )
    print("Sleeping...")
    time.sleep(5)
    print("Done sleeping.")
    # print(sync_squeaks_response)
    # assert peer_id in sync_squeaks_response.sync_result.completed_peer_ids

    # Get the squeak display item
    squeak_display_entry = get_squeak_display(
        other_admin_stub, saved_squeak_hash)
    assert squeak_display_entry.squeak_hash == saved_squeak_hash
