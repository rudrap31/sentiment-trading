import { Line } from "react-chartjs-2";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    scales,
} from "chart.js";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

function PortfolioChart({ portfolio }) {
    const value = Math.round(portfolio.value * 100) / 100;
    const percentage = (value - 100000) / 1000;
    const colors = value >= 100000 ? 'rgba(46, 204, 113, 1)' : 'rgba(207, 0, 25, 1)';
    const chartData = {
        labels: portfolio.value ? portfolio.value_log.map(item => item.time.split("T")[0]) : [],
        datasets: [
            {
                label: 'Portfolio Value',
                data: portfolio.value ? portfolio.value_log.map(item => item.value) : [],
                fill: 'origin',
                borderColor: colors,
                tension: 0.1
            }
        ]
    };
    const chartOptions = {
        datasets: {
            line: {
                borderWidth: 5,
                pointRadius: 0
            }
        },
        
        plugins: {
          legend: {
            display: false,
          },
        scales: {
            x: {
                
                grid: {
                    display: false,
                    drawTicks: false,
                    drawOnChartArea: false,
                },
            },
            y: {
                grid: {
                    display: false,
                    drawTicks: false,
                    drawOnChartArea: false,
                }
            }
        }
        },
        
      };

    return (
        <div className="chart">
            <div className="value">
                <h2>${value}</h2>
                <h3 style={{ color: colors}}>%{Math.round(percentage * 100) /100}</h3>
            </div>
            <Line data={chartData} options={chartOptions} />
            
        </div>
    );
}
export default PortfolioChart