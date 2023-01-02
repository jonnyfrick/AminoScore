import React, {  useState, useEffect } from 'react';
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
import { Tabula } from '.';



import './index.css'


ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);







export function Amino({apiData, setApiData}, ) {
  console.log('fresh start')
  



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
  





  const [foodIndex, setFoodIndex] = useState([0])

  //
  return <div className='container'>
    
    <Bar options={options} data={apiData} />
    <Tabula aminoArray={apiData.datasets} setApiData={setApiData} />
    
    
  </div>
}