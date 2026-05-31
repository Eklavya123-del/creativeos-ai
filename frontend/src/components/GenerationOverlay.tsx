
import { useEffect, useState } from "react"


const messages = [

  "Analyzing campaign...",

  "Retrieving creative memory...",

  "Understanding template composition...",

  "Building cinematic directions...",

  "Generating luxury advertising concepts..."
]


function GenerationOverlay() {

  const [index, setIndex] =
    useState(0)


  useEffect(() => {

    const interval = setInterval(() => {

      setIndex((prev) =>

        (prev + 1) %
        messages.length
      )

    }, 1800)

    return () =>
      clearInterval(interval)

  }, [])


  return (

    <div className="
      fixed
      inset-0
      z-[999]
      bg-black/70
      backdrop-blur-2xl
      flex
      items-center
      justify-center
    ">

      <div className="
        text-center
      ">

        {/* SPINNER */}
        <div className="
          w-20
          h-20
          border-4
          border-white/10
          border-t-white
          rounded-full
          animate-spin
          mx-auto
          mb-10
        " />



        {/* TITLE */}
        <h2 className="
          text-4xl
          font-black
          mb-5
        ">
          CreativeOS AI
        </h2>


        {/* MESSAGE */}
        <p className="
          text-zinc-400
          text-lg
          transition-all
          duration-500
        ">
          {messages[index]}
        </p>

      </div>

    </div>
  )
}

export default GenerationOverlay

