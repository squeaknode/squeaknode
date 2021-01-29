


function getImageSrcString(imageBase64) {
  return "data:image/jpeg;base64," + imageBase64;
}

export function getAuthorImageSrcString(squeak) {
  const authorImage = squeak.getAuthorImage();
  return getImageSrcString(authorImage);
}

export function getProfileImageSrcString(squeakProfile) {
  const profileImage = squeakProfile.getProfileImage();
  return getImageSrcString(profileImage);
}
