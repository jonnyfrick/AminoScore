import React, { useState, useEffect } from 'react';

import { Amino } from "./components/tabula/Amino"


export function App() {
  const labels = ['AminoA', 'AminoB', 'AminoC', 'AminoD', 'AminoE', 'AminoF', 'AminoG', 'AminoH', 'AminoI'];
  const colors = ['rgb(247,252,253)', 'rgb(224,236,244)', 'rgb(191,211,230)', 'rgb(158,188,218)', 'rgb(140,150,198)', 'rgb(140,107,177)', 'rgb(136,65,157)', 'rgb(129,15,124)', 'rgb(77,0,75)', 'rgb(10,10,10)']

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

  if (apiData.length < 2) {
    setApiData(preparedData())
  }
  console.log('please only at beginning')
  return <div>
    <Amino origData={apiData} />
  </div>
}


