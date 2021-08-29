import React from 'react';
import { useTheme } from '@material-ui/styles';
import ApexCharts from 'react-apexcharts';

const series = [
  {
    name: 'Metric1',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: 'Metric2',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: 'Metric3',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: 'Metric4',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: 'Metric5',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: 'Metric6',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: 'Metric7',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: 'Metric8',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
  {
    name: 'Metric9',
    data: generateData(18, {
      min: 0,
      max: 90,
    }),
  },
];

export default function ApexLineChart() {
  const theme = useTheme();

  return (
    <ApexCharts
      options={themeOptions(theme)}
      series={series}
      type="heatmap"
      height={350}
    />
  );
}

// ##################################################################
function generateData(count, yrange) {
  let i = 0;
  const series = [];
  while (i < count) {
    const x = `w${(i + 1).toString()}`;
    const y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

    series.push({
      x,
      y,
    });
    i++;
  }

  return series;
}

function themeOptions(theme) {
  return {
    chart: {
      toolbar: {
        show: false,
      },
    },
    dataLabels: {
      enabled: false,
    },
    colors: [theme.palette.primary.main],
  };
}
