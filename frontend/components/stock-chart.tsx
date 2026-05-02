"use client";

import { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  ComposedChart,
  Area,
  ReferenceLine,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface ChartData {
  date: string;
  price: number;
  volume: number;
  change?: number;
}

interface StockChartProps {
  ticker: string;
  data?: ChartData[];
  isLoading?: boolean;
}

export function StockChart({ ticker, data: initialData, isLoading }: StockChartProps) {
  const [chartData, setChartData] = useState<ChartData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (initialData) {
      setChartData(initialData);
      setLoading(false);
    } else {
      // Generate mock data if no data provided
      generateMockData();
    }
  }, [initialData]);

  const generateMockData = () => {
    const mockData: ChartData[] = [];
    const basePrice = 60000;
    const days = 30;
    
    for (let i = 0; i < days; i++) {
      const date = new Date();
      date.setDate(date.getDate() - (days - i));
      
      const randomChange = (Math.random() - 0.5) * 2000;
      const price = basePrice + randomChange + (i * 100);
      const volume = Math.floor(Math.random() * 1000000) + 500000;
      
      mockData.push({
        date: date.toLocaleDateString('vi-VN', { month: 'short', day: 'numeric' }),
        price: Math.round(price),
        volume: volume,
        change: i > 0 ? price - mockData[i - 1].price : 0,
      });
    }
    
    setChartData(mockData);
    setLoading(false);
  };

  if (loading || isLoading) {
    return (
      <Card>
        <CardHeader className="pb-3 sm:pb-4">
          <CardTitle className="text-sm sm:text-base">Biểu Đồ Giá {ticker}</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="h-48 sm:h-56 lg:h-64 flex items-center justify-center">
            <div className="animate-pulse">
              <div className="h-32 sm:h-40 lg:h-48 bg-gray-200 dark:bg-gray-700 rounded"></div>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  const maxPrice = Math.max(...chartData.map(d => d.price));
  const minPrice = Math.min(...chartData.map(d => d.price));
  const avgPrice = (maxPrice + minPrice) / 2;

  return (
    <Card>
      <CardHeader className="pb-3 sm:pb-4">
        <CardTitle className="flex items-center justify-between">
          <span className="text-sm sm:text-base">Biểu Đồ Giá {ticker}</span>
          <div className="text-xs sm:text-sm font-normal text-muted-foreground">
            {chartData.length} ngày
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-3 sm:space-y-4">
          {/* Price Chart */}
          <div className="h-48 sm:h-56 lg:h-64 w-full">
            <ResponsiveContainer width="100%" height="100%" minWidth={200}>
              <ComposedChart data={chartData}>
                <defs>
                  <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="priceGradientRed" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                <XAxis 
                  dataKey="date" 
                  stroke="#9ca3af"
                  fontSize={12}
                  tick={{ fill: '#9ca3af' }}
                />
                <YAxis 
                  stroke="#9ca3af"
                  fontSize={12}
                  tick={{ fill: '#9ca3af' }}
                  domain={['dataMin - 1000', 'dataMax + 1000']}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                  }}
                  itemStyle={{ color: '#f3f4f6' }}
                  labelStyle={{ color: '#9ca3af' }}
                  formatter={(value: any, name: any) => {
                    if (name === 'price') {
                      return [`₫${value.toLocaleString()}`, 'Giá'];
                    }
                    if (name === 'volume') {
                      return [`${(value / 1000000).toFixed(2)}M`, 'Khối lượng'];
                    }
                    return [value, name];
                  }}
                />
                <ReferenceLine 
                  y={avgPrice} 
                  stroke="#fbbf24" 
                  strokeDasharray="5 5" 
                  strokeWidth={2}
                />
                <Area
                  type="monotone"
                  dataKey="price"
                  stroke="#10b981"
                  strokeWidth={2}
                  fill="url(#priceGradient)"
                />
                <Line
                  type="monotone"
                  dataKey="price"
                  stroke="#ef4444"
                  strokeWidth={2}
                  dot={false}
                  hide={true}
                />
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          {/* Volume Chart */}
          <div className="h-24 sm:h-28 lg:h-32 w-full">
            <ResponsiveContainer width="100%" height="100%" minWidth={200}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                <XAxis 
                  dataKey="date" 
                  stroke="#9ca3af"
                  fontSize={12}
                  tick={{ fill: '#9ca3af' }}
                />
                <YAxis 
                  stroke="#9ca3af"
                  fontSize={12}
                  tick={{ fill: '#9ca3af' }}
                  tickFormatter={(value) => `${(value / 1000000).toFixed(1)}M`}
                />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: '1px solid #374151',
                    borderRadius: '8px',
                  }}
                  itemStyle={{ color: '#f3f4f6' }}
                  labelStyle={{ color: '#9ca3af' }}
                  formatter={(value: any) => [
                    `${(value / 1000000).toFixed(2)}M`,
                    'Khối lượng'
                  ]}
                />
                <Bar 
                  dataKey="volume" 
                  fill="#3b82f6"
                  opacity={0.7}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Summary Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t">
            <div className="text-center">
              <div className="text-sm text-muted-foreground">Giá hiện tại</div>
              <div className="text-lg font-semibold text-foreground">
                ₫{chartData[chartData.length - 1]?.price.toLocaleString()}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-muted-foreground">Thay đổi</div>
              <div className={`text-lg font-semibold ${
                (chartData[chartData.length - 1]?.change || 0) >= 0 
                  ? 'text-green-600 dark:text-green-400' 
                  : 'text-red-600 dark:text-red-400'
              }`}>
                {(chartData[chartData.length - 1]?.change || 0) >= 0 ? '+' : ''}
                ₫{Math.abs(chartData[chartData.length - 1]?.change || 0).toLocaleString()}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-muted-foreground">Cao nhất</div>
              <div className="text-lg font-semibold text-foreground">
                ₫{maxPrice.toLocaleString()}
              </div>
            </div>
            <div className="text-center">
              <div className="text-sm text-muted-foreground">Thấp nhất</div>
              <div className="text-lg font-semibold text-foreground">
                ₫{minPrice.toLocaleString()}
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
