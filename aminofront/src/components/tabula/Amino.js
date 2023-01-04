import React, { useState, useEffect, useMemo } from 'react';
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



export function Amino({ origData },) {

  

  //decouple apiData from this Child component - so that it doesnot rerender parent
  const [apiData, setApiData] = useState(origData);
  const [datasets, setDatasets] = useState(apiData.datasets)
  const [barData, setBarData] = useState(origData);



  useEffect(() => {
    setApiData(origData);
    setDatasets(origData.datasets)
    const chosenOrig = origData;
    const ds = chosenOrig.datasets;
    const newDs = ds.filter((ele) => ele.inchart === 'true')
    chosenOrig.datasets = newDs;
    setBarData(chosenOrig);

  }, [origData])

  const prepareBar = function prepper(data, origData) {
    const nextBarData = origData;
    const newDs = datasets.filter((ele) => ele.inchart === 'true')
    nextBarData.datasets = newDs;
    setBarData(nextBarData);
  }

  useMemo(() => {
    prepareBar(datasets, origData)
  }, [datasets])


  

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
  



  return <div className='container'>

    <Bar options={options} data={barData} />
    <Tabula aminoArray={datasets} setAminoArray={setDatasets} />


  </div>
}