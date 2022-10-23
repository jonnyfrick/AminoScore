import React, { Component } from 'react';
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
import { Products } from './components/Products'
import './index.css'
//import Chance from 'chance'
//const chance = new Chance();

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const mock_data = { "Peanut butter, creamy": [0.229, 0.806, 0.92, 1.88, 0.951, 0.29, 1.5, 1.06, 1.12, 0.676], "Soy milk, unsweetened, plain, shelf stable": [0.046, 0.128, 0.145, 0.249, 0.221, 0.046, 0.175, 0.124, 0.142, 0.098], "Flour, soy, defatted": [2.31, 4.11, 3.06, 2.31, 1.27, 0.616, 1.97, 0.622, 2.86, 1.74], "Flour, soy, full-fat": [1.74, 3.06, 2.14, 1.74, 0.95, 0.45, 1.48, 0.485, 2.15, 1.4], "Soy milk, unsweetened, plain, refrigerated": [0.034, 0.1, 0.1, 0.2, 0.2, 0.033, 0.157, 0.1, 0.101, 0.1] }


export const options = {
  plugins: {
    title: {
      display: true,
      text: 'AminoScore',
      font: {
        family: "Montserrat", // Add your font here to change the font of your y axis
        size: 30
      },
    },

    legend: {
      position: 'right',
      labels: {
        // This more specific font property overrides the global property
        font: {
          size: 10
        }
      },
    },


    scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true,
      },
    }
  },
};

const labels = ['AminoA', 'AminoB', 'AminoC', 'AminoD', 'AminoE', 'AminoF', 'AminoG', 'AminoH', 'AminoI'];


const colors = ['rgb(237,248,251)', 'rgb(179,205,227)', 'rgb(140,150,198)', 'rgb(136,86,167)', 'rgb(129,15,124)']


const datasets = []

Object.keys(mock_data).forEach((key, index) => {

  datasets.push({
    label: key,
    data: mock_data[key],
    backgroundColor: colors[index],
    stack: 'Stack 0',

  })

})

export const data = {
  labels,
  datasets,
};




export function App() {
  return <div className='container'>
    <div className='row'>
      <div className='left-panel box'>
        <Bar options={options} data={data} />
      </div>
      <div className='right-panel box'>
        <Products />
      </div>
    </div>
  </div>
}


