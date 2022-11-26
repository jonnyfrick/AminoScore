import React, { Component, useState } from 'react';
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
import { Tabula } from './components/tabula'


import './index.css'


ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);





//const [amArray, setAmArray] = useState(foodies);
//const fooditems = food;



/* const handleAddRam = () => {
  let arr = [...ram]
  arr.push(
    {
      id: 6,
      name: "sil wee",
      aminos: [0.229, 0.806, 0.92, 1.88, 0.951, 0.29, 1.5, 1.06, 1.12, 0.676],
      KCal: 50.95,
      description:
        "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
      category: "men's clothing",
      rating: {
        rate: 3.9,
        count: 120,
      },
    })
    ramChange(arr)
};

useEffect(() => {
  handleAddRam();
}, []); */


// const a = Object.values(fooditems).map((value, index) => {
//   return value.name

// });
 
// const ab = foodies
//const mock_data = { "Peanut butter, creamy": [0.229, 0.806, 0.92, 1.88, 0.951, 0.29, 1.5, 1.06, 1.12, 0.676], "Soy milk, unsweetened, plain, shelf stable": [0.046, 0.128, 0.145, 0.249, 0.221, 0.046, 0.175, 0.124, 0.142, 0.098], "Flour, soy, defatted": [2.31, 4.11, 3.06, 2.31, 1.27, 0.616, 1.97, 0.622, 2.86, 1.74], "Flour, soy, full-fat": [1.74, 3.06, 2.14, 1.74, 0.95, 0.45, 1.48, 0.485, 2.15, 1.4], "Soy milk, unsweetened, plain, refrigerated": [0.034, 0.1, 0.1, 0.2, 0.2, 0.033, 0.157, 0.1, 0.101, 0.1] }


export const options = {
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

export const food = [{
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

Object.values(food).forEach((val, index) => {
  datasets.push({
    label: val.name,
    data: val.aminos,
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
    <Bar options={options} data={data} />
    <Tabula food={food}/>
  </div>
}


