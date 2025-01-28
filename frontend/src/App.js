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
                    <h3 className="label">Active Trades:</h3>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Ticker</th>
                                <th>Headline</th>
                                <th>Action</th>
                                <th>Buy Price</th>
                                <th>Current Price</th>
                                <th>P/L</th>
                                <th>Amount</th>

                            </tr>
                        </thead>
                        <tbody>
                            {portfolio.stocks && Object.keys(portfolio.stocks).map(ticker => {
                                const stock = portfolio.stocks[ticker];
                                const plPercentage = stock.type === "BUY"
                                    ? (((stock.current_price - stock.buy_price) / stock.buy_price) * 100).toFixed(2)
                                    : (((stock.buy_price - stock.current_price) / stock.buy_price) * 100).toFixed(2);
                                return (
                                    <tr key={ticker}>
                                        <td>{new Date(stock.time).toLocaleString()}</td>
                                        <td>{ticker}</td>
                                        <td>{stock.headline}</td>
                                        <td>{stock.type}</td>
                                        <td>${stock.buy_price}</td>
                                        <td>${stock.current_price}</td>
                                        <td style={{
                                            color: plPercentage >= 0 ? 'rgba(46, 204, 113, 1)' : 'rgba(207, 0, 25, 1)',
                                            }}>%{plPercentage}</td>
                                        <td>{stock.quantity}</td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>

                <div>
                    <h3 className="label">Closed Trades</h3>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Time</th>
                                <th>Ticker</th>
                                <th>Headline</th>
                                <th>Action</th>
                                <th>Buy Price</th>
                                <th>Sold Price</th>
                                <th>Profit</th>
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
                                        <td>${trade.buy_price.toFixed(2)}</td>
                                        <td>${trade.sold_price.toFixed(2)}</td>
                                        <td style={{
                                            color: trade.profit >= 0 ? 'rgba(46, 204, 113, 1)' : 'rgba(207, 0, 25, 1)',
                                            }}> {trade.profit >= 0 ? `+${trade.profit.toFixed(2)}` : `${trade.profit.toFixed(2)}`}</td>
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
