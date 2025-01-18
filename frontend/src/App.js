import React, { useEffect, useState } from "react";
import axios from 'axios';  
import PortfolioChart from "./Line";
import "./App.css";

function App() {
    const [portfolio, setPortfolio] = useState([{}]);

    useEffect(() => {
        axios.get("http://127.0.0.1:5000/api/portfolio")
            .then((response) => {
                setPortfolio(response.data);  // Set portfolio to the data from the response
                console.log(response.data.value);  // Log the cash value
            })
            .catch((error) => {
                console.error('Error fetching portfolio:', error);  // Handle error if any
            });
    }, []);

    return (
        <div className="body">
            
            <PortfolioChart portfolio={portfolio} />
            <div>
                <div>
                    <h3>Trade History:</h3>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Ticker</th>
                                <th>Headline</th>
                                <th>Action</th>
                                <th>Price</th>
                                <th>Amount</th>
                                
                            </tr>
                        </thead>
                        <tbody>
                            {portfolio.trade_history && portfolio.trade_history.map((trade, index) => (
                                <tr key={index}>
                                    <td>{new Date(trade.time).toLocaleString()}</td>
                                    <td>{trade.ticker}</td>
                                    <td>{trade.headline}</td>
                                    <td>{trade.action}</td>
                                    
                                    <td>${trade.price.toFixed(2)}</td>
                                    <td>{trade.amount}</td>
                                    
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

export default App;
