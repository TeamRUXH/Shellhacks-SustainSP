import Link from "next/link"

import { siteConfig } from "@/config/site"
import { buttonVariants } from "@/components/ui/button"

export default function IndexPage() {
  return (
    <section className="container grid items-center gap-8 pb-8 pt-6 md:py-10" style={{ height: '100%', padding: '5rem' }}>
      <div className="flex flex-col items-center gap-2" style={{ alignItems: 'center', justifyContent: 'center' }}>
        <h1 className="text-4xl font-extrabold leading-tight tracking-tighter md:text-4xl" style={{ fontSize: '3rem', marginBottom: '1.5rem' }}>
          S&P Sustainability Dashboard 
        </h1>
        <p className="max-w-[700px] text-lg text-muted-foreground" style={{ margin: 'auto', textAlign: 'center' }}>
          Powered using High Performance Real-time Data Analysis and Machine Learning Algorithms.
        </p>
      </div>
      <div className="flex gap-4" style={{ justifyContent: 'center' }}>
        <Link
          href="/dashboard"
          className={buttonVariants()}
        >
          Visit Dashboard
        </Link>
        <Link
          target="_blank"
          rel="noreferrer"
          href={siteConfig.links.github}
          className={buttonVariants({ variant: "secondary" })}
        >
          GitHub
        </Link>
      </div>
    </section>
  )
}
