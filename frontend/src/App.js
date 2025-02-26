import React, { useEffect, useState } from "react";
import axios from 'axios';
import PortfolioChart from "./components/Line";
import Table from "./components/Table";
import "./App.css";
import { tailChase } from 'ldrs'

tailChase.register()

function App() {
    const [portfolio, setPortfolio] = useState([{}]);
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        setLoading(true);
        axios.get("https://sentiment-trading.onrender.com")
            .then((response) => {
                setPortfolio(response.data);  // Set portfolio to the data from the response
                setLoading(false)
            })
            .catch((error) => {
                console.error('Error fetching portfolio:', error);  // Handle error if any
                setLoading(false)
            });
    }, []);


    return (
        <div  className="body">
            {loading ? (
                <div class="loading">
                    <p>Loading data...</p>
                    <l-tail-chase
                        size="40"
                        speed="1.75"
                        color="white">
                    </l-tail-chase>
                </div>
            ) : (
                <div>
                    <PortfolioChart portfolio={portfolio} />
                    <Table portfolio={portfolio} />
                </div>
            )}
        </div>
    );
}

export default App;
