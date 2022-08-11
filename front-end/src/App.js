import logo from './logo.svg';
import './App.css';
import React, {useState, useEffect} from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import Table from 'react-bootstrap/Table';
import Form  from 'react-bootstrap/Form';
import InputGroup  from 'react-bootstrap/InputGroup';
import stocksView from './componets/StocksVew';

function App() {

  
  const[StockList,setStockList] = useState([])
  const [addStock, setAddStock] = useState('')
  useEffect( ()=> {fetchStocks();}, [] )
  // read all stocks
  const fetchStocks = () => {
    axios.get('http://127.0.0.1:8000/home')
    .then (res => { 
      setStockList(res.data)
      console.log(res.data)
      
    })
    .catch((err)=> {
      console.log(err)
    })
  };

  //post all stocks 
  const addStockHandler =  (event) =>{
    const newStock = {
      "symbol": addStock
  }
    
        axios.post('http://127.0.0.1:8000/stocks',{"symbol": addStock})
      .then(res => console.log(res))
  }

  return (
    <div className='App'>
      Welcome to Your Home Page

      <div className = "App list-group-item justify-content-center align-items-center mx-auto" 
      style = {{"width": "400px", "backgroundColor": "white",
        "marginTop":"5px"}}>
        <h1 className='card text-white bg-primary mb-1'
        styleName = "max-width: 20rem;">Stock Trading
        </h1>
      </div>
  

    <input className = "mb-2 form-control titleIn" 
    onChange={ e => setAddStock(e.target.value)}
    placeholder = "Enter Stock Symbol"></input>
    
    <button className='btn btn-outline-primart mx-2' 
     onClick={ e => addStockHandler(e)}> Add Stock </button>
    
     <div className = "mb-3" >
      <table striped bordered hover size ="sm" >
      <tbody>
        <tr>

          <th> Id</th> 
          <th> Symbol</th>
          <th> Forward_Price</th>
          <th> Price</th>
          <th> Forward_Eps</th>
          <th>Max50</th>
          
        </tr>
      
            {StockList.map((stock) =>(
       
          <tr>
          <td>{stock.id}  </td>
          <td>{stock.symbol}  </td>
          <td>{stock.forward_pe}  </td>
          <td>{stock.price}  </td>
          <td>{stock.forward_eps}  </td>
          <td>{stock.ma50}  </td>
          </tr>
        
        
      ))}
      </tbody>
     
      </table>
      </div>
    
    
    </div>
    
  );
}

export default App;

