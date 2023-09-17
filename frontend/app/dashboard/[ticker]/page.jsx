"use client"

import React, { useEffect, useState } from "react"
import { usePathname } from "next/navigation"
import axios from "axios"
import { Asterisk, Palmtree, ThumbsUp, Users } from "lucide-react"
import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
} from "recharts"

import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

function Box({ title, score, more, degree }) {
  return (
    <Card
      className="w-full"
      style={{
        background: `url(https://github.githubassets.com/images/modules/dashboard/universe23/bg.png)`,
        backgroundRepeat: "no-repeat",
        backgroundSize: "100%",
        backdropFilter: "blur(10px)",
        filter: `hue-rotate(${degree})`,
      }}
    >
      <CardHeader
        className="flex flex-row items-center justify-between space-y-0"
        style={{
          justifyContent: "space-between",
          paddingBottom: ".5rem",
          paddingTop: ".85rem",
        }}
      >
        <CardTitle className="text-md font-medium">{title}</CardTitle>
        {title == "Total ESG Risk Score" && (
          <Asterisk className="ml-2 h-8 w-8" />
        )}
        {title == "Environment Risk Score" && (
          <Palmtree className="ml-2 h-8 w-8" />
        )}
        {title == "Social Risk Score" && (
          <ThumbsUp mtree className="ml-2 h-8 w-8" />
        )}
        {title == "Governance Risk Score" && (
          <Users mtree className="ml-2 h-8 w-8" />
        )}
      </CardHeader>
      <CardContent style={{ marginBottom: "-.5rem" }}>
        <div className="text-3xl font-bold">{score}</div>
        {more && <p className="text-xs text-muted-foreground">{more}</p>}
      </CardContent>
    </Card>
  )
}

function Overview({ data }) {
  return (
    <ResponsiveContainer width="100%" height="100%">
      <LineChart
        data={Object.keys(data).map((key) => ({
          name: [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
          ][new Date(key / 1).getMonth()],
          total: data[key],
        }))}
      >
        <CartesianGrid
          stroke="rgba(255, 255, 255, .15)"
          strokeDasharray="5 5"
        />
        <XAxis
          dataKey="name"
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke="#888888"
          fontSize={12}
          tickLine={false}
          axisLine={false}
        />
        <Line
          type="monotone"
          dataKey="total"
          stroke="#8884d8"
          fill="rgb(255, 255, 255)"
          radius={[4, 4, 0, 0]}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

export default function TickerPage() {
  let ticker = usePathname()

  const [data, setData] = React.useState(null)

  React.useEffect(() => {
    axios
      .post("http://localhost:5000/company", {
        ticker: ticker.split("/")[ticker.split("/").length - 1],
      })
      .then(function (response) {
        setData(response.data)
      })
  }, [])

  if (!data)
    return (
      <div style={{ display: "grid", placeItems: "center", height: "30rem" }}>
        <svg
          width="48"
          height="48"
          xmlns="http://www.w3.org/2000/svg"
          style={{ transform: "scale(1.5)" }}
        >
          <path
            fill="#8884d8"
            d="M10.14,1.16a11,11,0,0,0-9,8.92A1.59,1.59,0,0,0,2.46,12,1.52,1.52,0,0,0,4.11,10.7a8,8,0,0,1,6.66-6.61A1.42,1.42,0,0,0,12,2.69h0A1.57,1.57,0,0,0,10.14,1.16Z"
          >
            <animateTransform
              attributeName="transform"
              type="rotate"
              dur="0.75s"
              values="0 12 12;360 12 12"
              repeatCount="indefinite"
            />
          </path>
        </svg>
      </div>
    )

  return (
    <section className="container grid items-center gap-6 pb-8 pt-6 md:py-10">
      <Card className="h-max">
        <CardContent className="px-8 py-4 h-max" style={{ paddingTop: "2rem" }}>
          <h1
            style={{ color: "#8884d8" }}
            className="text-3xl font-extrabold leading-tight tracking-tighter md:text-4xl"
          >
            {ticker.split("/")[ticker.split("/").length - 1]}
          </h1>

          <h3
            className="text-md leading-tight tracking-tighter"
            style={{ marginTop: ".5rem", marginBottom: "2rem" }}
          >
            Detailed Analysis and View
          </h3>

          <div className="flex-1 space-y-4 p-8">
            <Tabs defaultValue="overview" className="space-y-4">
              <TabsContent value="overview" className="space-y-4">
                <div className="flex flex-row space-x-4">
                  <Box
                    title="Total ESG Risk Score"
                    score={data["Total ESG Risk Score"]}
                    more={data["Total ESG Percentile"]}
                    degree={0}
                  />
                  <Box
                    title="Environment Risk Score"
                    score={data["Environment Risk Score"]}
                    degree={`-60deg`}
                  />
                  <Box
                    title="Social Risk Score"
                    score={data["Social Risk Score"]}
                    degree={`-70deg`}
                  />
                  <Box
                    title="Governance Risk Score"
                    score={data["Governance Risk Score"]}
                    degree={`-80deg`}
                  />
                </div>
              </TabsContent>
            </Tabs>
          </div>

          <div
            className="flex flex-row"
            style={{ justifyContent: "space-between", minHeight: "30rem" }}
          >
            <div
              className="flex flex-col"
              style={{
                width: "58%",
              }}
            >
              <h2
                className="text-2xl font-bold leading-tight tracking-tighter"
                style={{ margin: "3rem 0 1rem 0" }}
              >
                Trends over the last 12 months
              </h2>
              <Card style={{ borderRadius: "2px", height: "100%" }}>
                <CardContent
                  style={{
                    height: "100%",
                    backgroundColor: "rgba(155, 155, 155, .1)",
                    backdropFilter: "blur(5px)",
                    padding: 0,
                    paddingRight: "1rem",
                  }}
                >
                  <div
                    style={{
                      borderRadius: "4px",
                      padding: "1rem",
                      width: "100%",
                      height: "100%",
                    }}
                  >
                    <Overview data={data.trends} />
                  </div>
                </CardContent>
              </Card>
            </div>
            <div style={{ width: "40%" }}>
              <h2
                className="text-2xl font-bold leading-tight tracking-tighter"
                style={{ margin: "3rem 0 1rem 0" }}
              >
                Recent &nbsp;News&nbsp; & &nbsp;Sentimental &nbsp;Analysis
              </h2>

              <Card style={{ borderRadius: "2px" }}>
                <CardContent
                  style={{
                    color: "white",
                    fontSize: "1rem",
                    padding: "2rem",
                    borderRadius: "2px",
                    color: "white",
                    backgroundColor: "rgba(155, 155, 155, .1)",
                    backdropFilter: "blur(5px)",
                  }}
                >
                  {data["sentiment"]
                    .map(({ title, label, url, source }) => (
                      <div style={{ marginBottom: "1.5rem" }} key={title}>
                        <Badge style={{ marginBottom: ".5rem" }}>{label}</Badge>
                        <h5 style={{ fontSize: "14px" }}>{title}</h5>
                        <p
                          style={{
                            marginTop: "5px",
                            fontStyle: "italic",
                            fontSize: "12px",
                          }}
                        >
                          {source}
                        </p>
                      </div>
                    ))
                    .slice(0, 5)}
                </CardContent>
              </Card>
            </div>
          </div>
        </CardContent>
      </Card>
    </section>
  )
}
