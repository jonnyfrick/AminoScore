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

const mock_data =  { "Peanut butter, creamy": [0.229, 0.806, 0.92, 1.88, 0.951, 0.29, 1.5, 1.06, 1.12, 0.676], "Soy milk, unsweetened, plain, shelf stable": [0.046, 0.128, 0.145, 0.249, 0.221, 0.046, 0.175, 0.124, 0.142, 0.098], "Flour, soy, defatted": [2.31, 4.11, 3.06, 2.31, 1.27, 0.616, 1.97, 0.622, 2.86, 1.74], "Flour, soy, full-fat": [1.74, 3.06, 2.14, 1.74, 0.95, 0.45, 1.48, 0.485, 2.15, 1.4], "Soy milk, unsweetened, plain, refrigerated": [0.034, 0.1, 0.1, 0.2, 0.2, 0.033, 0.157, 0.1, 0.101, 0.1] }


export const options = {
  plugins: {
    title: {
      display: true,
      text: 'Stack your amino juice',
    },
  },
  responsive: true,
  interaction: {
    intersect: true,
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

const labels = ['AminoA', 'AminoB', 'AminoC', 'AminoD', 'AminoE', 'AminoF', 'AminoG', 'AminoH', 'AminoI'];


const colors = ['rgb(202,0,32)','rgb(244,165,130)','rgb(247,247,247)','rgb(146,197,222)','rgb(5,113,176)']


const datasets = []

function random_rgb() {
  var o = Math.round, r = Math.random, s = 255;
  return 'rgb(' + o(r()*s) + ',' + o(r()*s) + ',' + o(r()*s) + ',' + r().toFixed(1) + ')';
}


Object.keys(mock_data).forEach((key,index)=> {
  
  datasets.push({
    label: key, 
    data: mock_data[key], 
    backgroundColor: colors[index],
    stack: 'Stack 0'
  })

})

export const data = {
  labels,
  datasets,
};




export function App() {
  return <Bar options={options} data={data} />;
}


/*
const datasets = [{
  label: 'Apple',
  data: labels.map(() => chance.integer({ min: 0, max: 1000 })),
  backgroundColor: 'rgb(255, 99, 132)',
  stack: 'Stack 0',
},
{
  label: 'Cucumber',
  data: labels.map(() => chance.integer({ min: 0, max: 1000 })),
  backgroundColor: 'rgb(75, 192, 192)',
  stack: 'Stack 0',
},
{
  label: 'Blueberries',
  data: labels.map(() => chance.integer({ min: 0, max: 1000 })),
  backgroundColor: 'rgb(53, 162, 235)',
  stack: 'Stack 0',
},
]
*/

