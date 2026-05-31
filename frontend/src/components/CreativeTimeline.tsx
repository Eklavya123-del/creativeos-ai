
interface TimelineItem {

  campaign: string

  result: string

  timestamp: string
}


interface Props {

  history: TimelineItem[]
}


function CreativeTimeline({

  history

}: Props) {

  return (

    <div>

      {/* HEADER */}
      <div className="
        mb-6
      ">

        <p className="
          text-zinc-500
          text-sm
          uppercase
          tracking-[0.2em]
          mb-2
        ">
          Workflow Memory
        </p>

        <h2 className="
          text-3xl
          font-black
        ">
          Timeline
        </h2>

      </div>


      {/* EMPTY */}
      {history.length === 0 && (

        <div className="
          bg-white/[0.04]
          border
          border-white/10
          rounded-[24px]
          p-6
          backdrop-blur-xl
        ">

          <p className="
            text-zinc-500
            leading-relaxed
          ">
            Generated campaigns
            will appear here.
          </p>

        </div>
      )}


      {/* ITEMS */}
      <div className="
        space-y-5
      ">

        {history.map((item, index) => (

          <div

            key={index}

            className="
              bg-white/[0.04]
              border
              border-white/10
              rounded-[24px]
              p-5
              backdrop-blur-xl
            "
          >

            <div className="
              flex
              items-start
              gap-4
            ">

              {/* DOT */}
              <div className="
                w-3
                h-3
                rounded-full
                bg-white
                mt-2
              " />


              {/* CONTENT */}
              <div>

                <h3 className="
                  font-bold
                  text-lg
                  mb-2
                ">
                  {item.campaign}
                </h3>

                <p className="
                  text-zinc-400
                  text-sm
                  mb-3
                ">
                  {item.result}
                </p>

                <p className="
                  text-zinc-600
                  text-xs
                ">
                  {item.timestamp}
                </p>

              </div>

            </div>

          </div>
        ))}

      </div>

    </div>
  )
}

export default CreativeTimeline

