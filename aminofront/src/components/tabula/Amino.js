import React, { Component, useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import axios from 'axios';

import { Bar } from 'react-chartjs-2';
import { Tabula } from '.';
import { Fetch } from './Fetch';


import './index.css'


ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);


async function getFoodsStuffNow() {
  try {
    let response = await fetch('http://localhost:8000/get_foods/?Restriction="vegan"');
    let responseJson = await response.json();
    return responseJson;
   } catch(error) {
    console.error(error);
  }
}
console.log(getFoodsStuffNow())


export function Amino() {
  const food = [{
    id: 1,
    name: "Peanutz butter, creamy",
    aminos: [0.229, 0.806, 0.92, 1.88, 0.951, 0.29, 1.5, 1.06, 1.12, 0.676],
    KCal: 50.95
  },
  {
    id: 2,
    name: "Soy milk, unsweetened, plain, shelf stable",
    aminos: [0.046, 0.128, 0.145, 0.249, 0.221, 0.046, 0.175, 0.124, 0.142, 0.098],
    KCal: 209.95
  },
  {
    id: 3,
    name: "Flour, soy, defatted",
    aminos: [2.31, 4.11, 3.06, 2.31, 1.27, 0.616, 1.97, 0.622, 2.86, 1.74],
    KCal: 259.95
  },
  {
    id: 4,
    name: "Flour, soy, full-fat",
    aminos: [1.74, 3.06, 2.14, 1.74, 0.95, 0.45, 1.48, 0.485, 2.15, 1.4],
    KCal: 259.95
  },
  {
    id: 5,
    name: "Soy milk, unsweetened, plain, refrigerated",
    aminos: [0.034, 0.1, 0.1, 0.2, 0.2, 0.033, 0.157, 0.1, 0.101, 0.1],
    KCal: 259.95
  }]

  const labels = ['AminoA', 'AminoB', 'AminoC', 'AminoD', 'AminoE', 'AminoF', 'AminoG', 'AminoH', 'AminoI'];
  const colors = ['rgb(237,248,251)', 'rgb(179,205,227)', 'rgb(140,150,198)', 'rgb(136,86,167)', 'rgb(129,15,124)']


  const datasets = []


  const options = {
    responsive: true,
    maintainAspectRatio: true,
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
        position: 'chartArea',
        align: 'start',
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

  const [currentFood, setCurrentFood] = useState(food);

  useEffect(() => {
    const datTrial = function getData() {
      const datasets = []
      Object.values(currentFood).forEach((val, index) => {
        datasets.push({
          label: val.name,
          data: val.aminos,
          backgroundColor: colors[index],
          stack: 'Stack 0',
        })
      });
      return {
        labels,
        datasets,
      };
    }
    setCurrentData(datTrial)
  }, [currentFood]);
  

  const datTrial = function getData() {
    const datasets = []
    Object.values(currentFood).forEach((val, index) => {
      datasets.push({
        label: val.name,
        data: val.aminos,
        backgroundColor: colors[index],
        stack: 'Stack 0',
      })
    });
    return {
      labels,
      datasets,
    };
  }
  const [currentData, setCurrentData] = useState(datTrial);

  //const [currentData, setCurrentData] = useState(datTrial)


  return <div className='container'>
    <Bar options={options} data={currentData} />
    <Tabula aminoArray ={currentFood} setAminoArray={setCurrentFood} />
  </div>
}