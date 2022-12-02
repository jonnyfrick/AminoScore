//import axios from "axios";
import React, { useMemo, useState } from "react";
import { useGlobalFilter, useSortBy, useTable } from "react-table";
import tw from "twin.macro";
import { GlobalFilter } from "./globalFilter";

const Table = tw.table`
  table-auto
  text-base
  text-gray-700
`;

const TableHead = tw.thead`
  p-5
`;

const TableRow = tw.tr`
border
border-blue-500
p-2
`;

const TableHeader = tw.th`
border
border-blue-500
p-2
max-w-sm
`;

const TableBody = tw.tbody`
max-w-sm

`;

const TableData = tw.td`
border
border-purple-900
p-2
`;

const Button = tw.button`
  pl-4
  pr-4
  pt-2
  pb-2
  text-black
  rounded-md
  bg-purple-400
  hover:bg-green-200
  transition-colors
`;


export function Tabula({aminoArray, setAminoArray}) {

 
 

  const columns = useMemo(
    () => [
      {
        Header: "Id",
        accessor: "id",
      },
      {
        Header: "KCal",
        accessor: "KCal",
      },
      {
        Header: "Name",
        accessor: "name",
      },
    ],
    []
  );
  

  const fetchAminos = (id) => {
    return aminoArray[id].aminos
  }
  
  const deleteAminos = (id) => {
    setAminoArray(current => 
      current.filter(obj => {
        return obj.id !== id
      })
    );
  };


  const tableHooks = (hooks) => {
    hooks.visibleColumns.push((columns) => [
      ...columns,
      {
        id: "Edit",
        Header: "Edit",
        Cell: ({ row }) => (
          <Button onClick={() => deleteAminos(row.values.id)}>
            Del
          </Button>
          
        ),
      },
    ]);
  };

  const tableInstance = useTable(
    {
      columns: columns,
      data: aminoArray,
    },
    useGlobalFilter,
    tableHooks,
    useSortBy
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    preGlobalFilteredRows,
    setGlobalFilter,
    state,
  } = tableInstance;

  // useEffect(() => {
  //   fetchProducts();
  // }, []);

  const isEven = (idx) => idx % 2 === 0;

  return (
    <>
      <GlobalFilter
        preGlobalFilteredRows={preGlobalFilteredRows}
        setGlobalFilter={setGlobalFilter}
        globalFilter={state.globalFilter}
      />
      <Table {...getTableProps()}>
        <TableHead>
          {headerGroups.map((headerGroup) => (
            <TableRow {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <TableHeader
                  {...column.getHeaderProps(column.getSortByToggleProps())}
                >
                  {column.render("Header")}
                  {column.isSorted ? (column.isSortedDesc ? " ▼" : " ▲") : ""}
                </TableHeader>
              ))}
            </TableRow>
          ))}
        </TableHead>
        <TableBody {...getTableBodyProps()}>
          {rows.map((row, idx) => {
            prepareRow(row);

            return (
              <TableRow
                {...row.getRowProps()}
                className={isEven(idx) ? "bg-slate-700 bg-opacity-30" : ""}
              >
                {row.cells.map((cell, idx) => (
                  <TableData {...cell.getCellProps()}>
                    {cell.render("Cell")}
                  </TableData>
                ))}
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </>
  );
}