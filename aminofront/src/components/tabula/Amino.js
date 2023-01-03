import React, { useState, useEffect } from 'react';
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
  console.log('run animo')
  
  //decouple apiData from this Child component - so that it doesnot rerender parent
  const [apiData, setApiData] = useState(origData);
  useEffect(() => {
    setApiData(origData);
  },[origData])



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


  const [tableIndex, setTableIndex] = useState(0)

  useEffect(() => {
    
    if (apiData.datasets.length>1){
      const clone = apiData
      let obj = clone.datasets[tableIndex];
      console.log(obj, tableIndex)
      if (obj.inchart==='true'){
        obj.inchart = 'false';
      }
      else{
        obj.inchart = 'true';
      }
      clone.datasets[tableIndex] = obj;
      setApiData(clone)
      
  
      

    }
    console.log('hea')

    /*
    let correctLine = apiData.datasets.find(f => f.id === tableIndex)

    setApiData({...apiData,
      datasets: apiData.datasets.find(f => f.id === tableIndex)?.inchart='true'
    })
    console.log('woiked?')
    /*
    apiData.datasets.map(ele => {
      if (ele.id === tableIndex) {

      }
    })
    Object.entries(apiData).forEach(([key, value]) => {
      if (key !== 'datasets') {
        gluedBack.push({
          labels: value
        });
      }
      else {
        const aRays = Object.entries(apiData.datasets).forEach(([key, value])=> {
          return value;
        })
        console.log('sta')
      }

    });

    if (apiData.datasets[tableIndex].inchart === 'true') {
      apiData.datasets[tableIndex].inchart = 'false'
    }
    else {
      apiData.datasets[tableIndex].inchart = 'true'
    }*/
    /*
    const addAminos = (id) => {
      let newAminoArray = [...aminoArray];
      if (newAminoArray[id].inchart === "true"){
        newAminoArray[id].inchart = "false";
        
  
      }
      else{
        newAminoArray[id].inchart = "true";
      }
      setAminoIndex(newAminoArray)
    };*/


  }, [tableIndex]);

  //
  return <div className='container'>

    <Bar options={options} data={apiData} />
    <Tabula aminoArray={apiData.datasets} setAminoIndex={setTableIndex} />


  </div>
}