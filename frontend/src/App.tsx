
import { useEffect, useState } from "react"

import "./App.css"

import GenerationOverlay from "./components/GenerationOverlay"
import CreativeTimeline from "./components/CreativeTimeline"
import ProductLibrary from "./components/ProductLibrary"
import TemplateLibrary from "./components/TemplateLibrary"
import Login from "./pages/Login"

type Variant = {

  name: string

  image: string

  prompt?: string

  description?: string
}


type TimelineItem = {

  campaign: string

  result: string

  timestamp: string
}
const API_URL =
  import.meta.env.VITE_API_URL

function App() {

  // -----------------------------------
  // WORKFLOW STATE
  // -----------------------------------
  const [campaign, setCampaign] =
    useState("")

  const [ratio, setRatio] =
    useState("square")

  const [style, setStyle] =
    useState("premium")

  const [selectedProducts,
  setSelectedProducts] =
    useState<string[]>([])

  const [selectedTemplate,
  setSelectedTemplate] =
    useState("")

  const [variants, setVariants] =
    useState<Variant[]>([])

  const [selectedVariant,
  setSelectedVariant] =
    useState<Variant | null>(null)

  const [loading, setLoading] =
    useState(false)

  const [history, setHistory] =
    useState<TimelineItem[]>([])
  
  const [isLoggedIn, setIsLoggedIn] =
    useState(false)



  // -----------------------------------
  // RESET TEMPLATE WHEN
  // RATIO CHANGES
  // -----------------------------------
  useEffect(() => {

    setSelectedTemplate("")

  }, [ratio])


  // -----------------------------------
  // PRODUCT SELECTION
  // -----------------------------------
  const handleProductSelect = (
    product: string
  ) => {

    if (
      selectedProducts.includes(
        product
      )
    ) {

      setSelectedProducts(

        selectedProducts.filter(
          (p) => p !== product
        )
      )

    } else {

      setSelectedProducts([
        ...selectedProducts,
        product
      ])
    }
  }


  // -----------------------------------
  // AI GENERATION
  // -----------------------------------
  const generateAIWorkflow =
    async () => {

      // -----------------------------------
      // VALIDATION
      // -----------------------------------
      if (!campaign) {

        alert(
          "Enter campaign brief"
        )

        return
      }

      if (!selectedTemplate) {

        alert(
          "Select template"
        )

        return
      }

      if (
        selectedProducts.length === 0
      ) {

        alert(
          "Select at least one product"
        )

        return
      }

      try {

        setLoading(true)

        const formData =
          new FormData()

        formData.append(
          "campaign",
          campaign
        )

        formData.append(
          "style",
          style
        )

        formData.append(
          "ratio",
          ratio
        )

        formData.append(
          "template_name",
          selectedTemplate
        )

        formData.append(
          "selected_products",

          selectedProducts.join(",")
        )

        const response = await fetch(

          "${API_URL}/generate-ai-creative",

          {
            method: "POST",
            body: formData
          }
        )

        const data =
          await response.json()

        console.log(data)

        if (!data.variants) {

          alert(
            "Generation failed"
          )

          return
        }

        setVariants(
          data.variants
        )

        setSelectedVariant(
          data.variants[0]
        )

        // -----------------------------------
        // TIMELINE
        // -----------------------------------
        setHistory((prev) => [

          {
            campaign,

            result:
              `${data.variants.length} AI creative directions generated`,

            timestamp:
              new Date()
                .toLocaleString()
          },

          ...prev
        ])

      } catch (error) {

        console.error(error)

        alert(
          "Generation failed"
        )

      } finally {

        setLoading(false)
      }
    }
  
  if (!isLoggedIn) {

    return (

      <Login
        onLogin={() =>
          setIsLoggedIn(true)
        }
      />
    )
  }



  return (

    <div className="
      min-h-screen
      bg-[#050505]
      text-white
      overflow-hidden
    ">

      {/* ----------------------------------- */}
      {/* BACKGROUND GRADIENTS */}
      {/* ----------------------------------- */}
      <div className="
        fixed
        top-0
        left-0
        w-full
        h-full
        pointer-events-none
        overflow-hidden
      ">

        <div className="
          absolute
          top-[-200px]
          left-[-200px]
          w-[500px]
          h-[500px]
          rounded-full
          bg-purple-500/10
          blur-[160px]
        " />

        <div className="
          absolute
          bottom-[-200px]
          right-[-200px]
          w-[500px]
          h-[500px]
          rounded-full
          bg-blue-500/10
          blur-[160px]
        " />

      </div>


      {/* ----------------------------------- */}
      {/* OVERLAY */}
      {/* ----------------------------------- */}
      {loading && (
        <GenerationOverlay />
      )}


      {/* ----------------------------------- */}
      {/* MAIN LAYOUT */}
      {/* ----------------------------------- */}
      <div className="
        relative
        z-10
        grid
        grid-cols-1
        xl:grid-cols-[340px_1fr_420px]
        min-h-screen
      ">

        {/* =================================== */}
        {/* LEFT SIDEBAR */}
        {/* =================================== */}
        <div className="
          border-r
          border-white/10
          bg-white/[0.03]
          backdrop-blur-2xl
          p-8
          overflow-y-auto
        ">

          {/* LOGO */}
          <div className="
            mb-12
          ">

            <p className="
              text-zinc-500
              text-sm
              uppercase
              tracking-[0.3em]
              mb-4
            ">
              AI Creative Workflow
            </p>

            <h1 className="
              text-6xl
              font-black
              tracking-tight
              leading-none
            ">
              CreativeOS
            </h1>

            <p className="
              text-zinc-500
              mt-5
              leading-relaxed
            ">
              AI-powered cinematic
              campaign generation
              workspace for modern
              wellness brands.
            </p>

          </div>


          {/* CAMPAIGN */}
          <div className="
            mb-8
          ">

            <label className="
              text-sm
              text-zinc-500
              mb-3
              block
              uppercase
              tracking-[0.2em]
            ">
              Campaign Brief
            </label>

            <textarea

              value={campaign}

              onChange={(e) =>
                setCampaign(
                  e.target.value
                )
              }

              placeholder="
Launch premium sleep gummies
for modern professionals...
              "

              className="
                w-full
                h-40
                resize-none
                rounded-[32px]
                bg-white/[0.04]
                border
                border-white/10
                p-6
                outline-none
                text-white
                leading-relaxed
                placeholder:text-zinc-600
                backdrop-blur-xl
              "
            />

          </div>


          {/* RATIO */}
          <div className="
            mb-6
          ">

            <label className="
              text-sm
              text-zinc-500
              mb-3
              block
              uppercase
              tracking-[0.2em]
            ">
              Output Ratio
            </label>

            <select

              value={ratio}

              onChange={(e) =>
                setRatio(
                  e.target.value
                )
              }

              className="
                w-full
                rounded-[24px]
                bg-white/[0.04]
                border
                border-white/10
                px-5
                py-4
                outline-none
                backdrop-blur-xl
              "
            >

              <option value="square">
                Square
              </option>

              <option value="story">
                Story
              </option>

              <option value="feed">
                Feed
              </option>

              <option value="banner">
                Banner
              </option>

            </select>

          </div>


          {/* STYLE */}
          <div className="
            mb-10
          ">

            <label className="
              text-sm
              text-zinc-500
              mb-3
              block
              uppercase
              tracking-[0.2em]
            ">
              Creative Direction
            </label>

            <select

              value={style}

              onChange={(e) =>
                setStyle(
                  e.target.value
                )
              }

              className="
                w-full
                rounded-[24px]
                bg-white/[0.04]
                border
                border-white/10
                px-5
                py-4
                outline-none
                backdrop-blur-xl
              "
            >

              <option value="premium">
                Premium
              </option>

              <option value="cinematic">
                Cinematic
              </option>

              <option value="editorial">
                Editorial
              </option>

              <option value="minimal">
                Minimal
              </option>

            </select>

          </div>


          {/* GENERATE BUTTON */}
          <button

            onClick={
              generateAIWorkflow
            }

            className="
              w-full
              rounded-[28px]
              bg-white
              text-black
              py-5
              font-bold
              text-lg
              hover:scale-[1.02]
              transition-all
              duration-300
              shadow-2xl
            "
          >
            Generate AI Campaign
          </button>


          {/* TIMELINE */}
          <div className="
            mt-14
          ">

            <CreativeTimeline
              history={history}
            />

          </div>

        </div>


        {/* =================================== */}
        {/* CENTER WORKSPACE */}
        {/* =================================== */}
        <div className="
          p-10
          overflow-y-auto
        ">

          {/* HEADER */}
          <div className="
            flex
            items-center
            justify-between
            mb-10
          ">

            <div>

              <p className="
                text-zinc-500
                uppercase
                tracking-[0.2em]
                text-sm
                mb-3
              ">
                AI Workspace
              </p>

              <h2 className="
                text-5xl
                font-black
              ">
                Creative Directions
              </h2>

            </div>

          </div>


          {/* MAIN PREVIEW */}
          <div className="
            bg-white/[0.04]
            border
            border-white/10
            rounded-[40px]
            p-8
            mb-10
            backdrop-blur-2xl
          ">

            {selectedVariant ? (

              <>

                {/* IMAGE */}
                <img

                  src={`${API_URL}/${selectedVariant.image}`}

                  alt={selectedVariant.name}

                  className="
                    w-full
                    rounded-[32px]
                    shadow-2xl
                    mb-8
                  "
                />


                {/* INFO */}
                <div className="
                  grid
                  xl:grid-cols-2
                  gap-8
                ">

                  {/* LEFT */}
                  <div>

                    <p className="
                      text-zinc-500
                      text-sm
                      uppercase
                      tracking-[0.2em]
                      mb-3
                    ">
                      AI Direction
                    </p>

                    <h2 className="
                      text-5xl
                      font-black
                      mb-6
                    ">
                      {selectedVariant.name}
                    </h2>

                    <p className="
                      text-zinc-300
                      leading-relaxed
                      text-lg
                    ">
                      {
                        selectedVariant.description
                      }
                    </p>

                  </div>


                  {/* RIGHT */}
                  <div className="
                    bg-white/[0.04]
                    border
                    border-white/10
                    rounded-[32px]
                    p-6
                    backdrop-blur-xl
                  ">

                    <p className="
                      text-zinc-500
                      text-sm
                      uppercase
                      tracking-[0.2em]
                      mb-4
                    ">
                      AI Creative Prompt
                    </p>

                    <div className="
                      max-h-[350px]
                      overflow-y-auto
                    ">

                      <p className="
                        text-zinc-300
                        leading-relaxed
                        whitespace-pre-wrap
                      ">
                        {
                          selectedVariant.prompt
                        }
                      </p>

                    </div>

                  </div>

                </div>

              </>

            ) : (

              <div className="
                h-[700px]
                flex
                items-center
                justify-center
              ">

                <div className="
                  text-center
                ">

                  <h2 className="
                    text-4xl
                    font-black
                    mb-4
                  ">
                    Creative Workspace
                  </h2>

                  <p className="
                    text-zinc-500
                    text-lg
                  ">
                    Generate cinematic
                    AI-powered campaign
                    directions to begin.
                  </p>

                </div>

              </div>
            )}

          </div>


          {/* VARIANTS */}
          {variants.length > 0 && (

            <div>

              <div className="
                flex
                items-center
                justify-between
                mb-6
              ">

                <h2 className="
                  text-3xl
                  font-black
                ">
                  AI Variants
                </h2>

                <p className="
                  text-zinc-500
                ">
                  {variants.length}
                  generated directions
                </p>

              </div>

              <div className="
                grid
                grid-cols-2
                xl:grid-cols-4
                gap-6
              ">

                {variants.map((variant) => (

                  <div

                    key={variant.name}

                    onClick={() =>
                      setSelectedVariant(
                        variant
                      )
                    }

                    className={`
                      cursor-pointer
                      rounded-[32px]
                      overflow-hidden
                      border
                      transition-all
                      duration-300
                      bg-white/[0.04]
                      backdrop-blur-xl
                      hover:scale-[1.02]

                      ${
                        selectedVariant?.name ===
                        variant.name

                        ? "border-white"

                        : "border-white/10"
                      }
                    `}
                  >

                    <img

                      src={`${API_URL}/${variant.image}`}

                      alt={variant.name}

                      className="
                        w-full
                      "
                    />

                    <div className="
                      p-5
                    ">

                      <h3 className="
                        text-xl
                        font-bold
                        mb-2
                      ">
                        {variant.name}
                      </h3>

                      <p className="
                        text-zinc-500
                        text-sm
                        line-clamp-3
                      ">
                        {
                          variant.description
                        }
                      </p>

                    </div>

                  </div>
                ))}

              </div>

            </div>
          )}

        </div>


        {/* =================================== */}
        {/* RIGHT PANEL */}
        {/* =================================== */}
        <div className="
          border-l
          border-white/10
          bg-white/[0.03]
          backdrop-blur-2xl
          p-8
          overflow-y-auto
          space-y-10
        ">

          {/* PRODUCTS */}
          <ProductLibrary

            selectedProducts={
              selectedProducts
            }

            onSelect={
              handleProductSelect
            }
          />


          {/* TEMPLATES */}
          <TemplateLibrary

            ratio={ratio}

            selectedTemplate={
              selectedTemplate
            }

            onSelect={
              setSelectedTemplate
            }
          />

        </div>

      </div>

    </div>
  )
}

export default App

