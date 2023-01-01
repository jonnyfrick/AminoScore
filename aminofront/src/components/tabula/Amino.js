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



import './index.css'


ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);







export function Amino() {
  console.log('fresh start')
  const labels = ['AminoA', 'AminoB', 'AminoC', 'AminoD', 'AminoE', 'AminoF', 'AminoG', 'AminoH', 'AminoI'];
  //const colors = ['rgb(237,248,251)', 'rgb(179,205,227)', 'rgb(140,150,198)', 'rgb(136,86,167)', 'rgb(129,15,124)', 'rgb(129,15,124)']
  const colors = ['rgb(247,252,253)','rgb(224,236,244)','rgb(191,211,230)','rgb(158,188,218)','rgb(140,150,198)','rgb(140,107,177)','rgb(136,65,157)','rgb(129,15,124)','rgb(77,0,75)', 'rgb(10,10,10)']
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
  const initialFood = [{
    id: 999,
    name: "pppp",
    aminos: [0.229, 0.806, 0.92, 1.88, 0.951, 0.29, 1.5, 1.06, 1.12, 0.676],
    KCal: 1,
    inchart: "false"
  },
  ]


  const preparedData = function getData() {
    const datasets = []
    Object.values(initialFood).forEach((val, index) => {
      datasets.push({
        label: val.name,
        name: val.name,
        id: val.id,
        data: val.aminos,
        aminos: val.aminos,
        Kcal: 1,
        inchart: 'false',
        backgroundColor: colors[index],
        stack: 'Stack 0',
      })
    });
    return {
      labels,
      datasets,
    };
  }
  

  const [apiData, setApiData] = useState([preparedData]);
  useEffect(() => {
    const arr = []
    const getDatas = async () => {
      let response = await fetch('http://localhost:8000/get_via_serializer/');
      let responseJson = await response.json();
      const top10 = responseJson.slice(0, 10);
      top10.forEach((element, i) => {
        arr.push({
          id: i,
          name: element.food_name,
          aminos: [element.Histidine, element.Isoleucine, element.Leucine, element.Lysine, element.Methionine, element.Phenylalanine, element.Threonine, element.Tryptophan, element.Tryptophan, element.Valine],
          KCal: 50,
          inchart: "false"
        })
      });
      const datasets = []
      const meshStuff = function mixIt() {
        const datasets = []
        Object.values(arr).forEach((val, index) => {

          datasets.push({
            label: val.name,
            name: val.name,
            id: val.id,
            data: val.aminos,
            aminos: val.aminos,
            Kcal: 1,
            inchart: 'false',
            backgroundColor: colors[index],
            stack: 'Stack 0',
          })

        });
        return {
          labels,
          datasets,
        };
      }
      setApiData(meshStuff)
    }
    getDatas()

  }, []);

  console.log('do we have datas?')


  if (apiData.length < 2){
    setApiData(preparedData())
  }
    



  return <div className='container'>
    <Bar options={options} data={apiData} />
    <Tabula aminoArray={apiData.datasets} setAminoArray={setApiData} />
  </div>
}