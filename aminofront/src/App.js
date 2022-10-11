import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar } from 'react-chartjs-2';
import Chance from 'chance'
const chance = new Chance();

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export const options = {
  plugins: {
    title: {
      display: true,
      text: 'Stack your amino juice',
    },
  },
  responsive: true,
  interaction: {
    intersect: false,
  },
  scales: {
    x: {
      stacked: true,
    },
    y: {
      stacked: true,
    },
  },
};

const labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

export const data = {
  labels,
  datasets: [
    {
      label: 'Apple',
      data: labels.map(() => chance.integer({ min: -1000, max: 1000 })),
      backgroundColor: 'rgb(255, 99, 132)',
      stack: 'Stack 0',
    },
    {
      label: 'Cucumber',
      data: labels.map(() => chance.integer({ min: -1000, max: 1000 })),
      backgroundColor: 'rgb(75, 192, 192)',
      stack: 'Stack 0',
    },
    {
      label: 'Blueberries',
      data: labels.map(() => chance.integer({ min: -1000, max: 1000 })),
      backgroundColor: 'rgb(53, 162, 235)',
      stack: 'Stack 1',
    },
  ],
};

export function App() {
  return <Bar options={options} data={data} />;
}
