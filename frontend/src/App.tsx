import { useState } from "react"

import ProductLibrary from "./components/ProductLibrary"
import TemplateLibrary from "./components/TemplateLibrary"
import CreativeTimeline from "./components/CreativeTimeline"

const API_URL =
  import.meta.env.VITE_API_URL

function App() {

  const [selectedProducts, setSelectedProducts] =
    useState<string[]>([])

  const [selectedTemplate, setSelectedTemplate] =
    useState("")

  const [generatedImage, setGeneratedImage] =
    useState("")

  const [loading, setLoading] =
    useState(false)

  const [history, setHistory] =
    useState<any[]>([])

  const [prompt, setPrompt] =
    useState(
      "Launch premium sleep gummies for modern professionals with cinematic wellness aesthetic"
    )

  const [ratio, setRatio] =
    useState("square")

  const [creativeStyle, setCreativeStyle] =
    useState("premium")


  // ============================================
  // PRODUCT SELECT
  // ============================================

  const toggleProduct = (
    product: string
  ) => {

    setSelectedProducts((prev) => {

      if (prev.includes(product)) {

        return prev.filter(
          (p) => p !== product
        )
      }

      return [...prev, product]
    })
  }


  // ============================================
  // GENERATE AI WORKFLOW
  // ============================================

  const generateAIWorkflow =
    async () => {

      try {

        if (
          selectedProducts.length === 0
        ) {

          alert(
            "Please select a product"
          )

          return
        }

        if (!selectedTemplate) {

          alert(
            "Please select a template"
          )

          return
        }

        setLoading(true)

        const formData =
          new FormData()

        formData.append(
          "campaign",
          prompt
        )

        formData.append(
          "ratio",
          ratio
        )

        formData.append(
          "style",
          creativeStyle
        )

        formData.append(
          "selected_products",
          JSON.stringify(
            selectedProducts
          )
        )

        formData.append(
          "template_name",
          selectedTemplate
        )

        const response =
          await fetch(

            `${API_URL}/generate-ai-creative`,

            {
              method: "POST",
              body: formData
            }
          )

        const data =
          await response.json()

        console.log(data)

        if (data.generated_image) {

          const imageUrl =
            `${API_URL}${data.generated_image}`

          setGeneratedImage(
            imageUrl
          )

          setHistory((prev) => [

            {
              image: imageUrl,
              prompt,
              ratio,
              style: creativeStyle
            },

            ...prev
          ])
        }

      } catch (error) {

        console.error(error)

        alert(
          "Generation failed"
        )

      } finally {

        setLoading(false)
      }
    }


  return (

    <div className="
      min-h-screen
      bg-black
      text-white
      flex
      overflow-hidden
    ">

      {/* LEFT PANEL */}

      <div className="
        w-[340px]
        border-r
        border-white/10
        p-8
        overflow-y-auto
        bg-gradient-to-b
        from-[#0f0f14]
        to-black
      ">

        <p className="
          text-xs
          tracking-[0.4em]
          uppercase
          text-zinc-500
          mb-6
        ">
          AI Creative Workflow
        </p>

        <h1 className="
          text-6xl
          font-black
          leading-none
          mb-8
        ">
          CreativeOS
        </h1>

        <p className="
          text-zinc-500
          text-lg
          leading-relaxed
          mb-14
        ">
          AI-powered cinematic campaign
          generation workspace for modern
          wellness brands.
        </p>


        {/* PROMPT */}

        <div className="mb-10">

          <p className="
            text-xs
            uppercase
            tracking-[0.3em]
            text-zinc-500
            mb-4
          ">
            Campaign Brief
          </p>

          <textarea

            value={prompt}

            onChange={(e) =>
              setPrompt(
                e.target.value
              )
            }

            className="
              w-full
              h-40
              rounded-[30px]
              bg-white/[0.04]
              border
              border-white/10
              p-6
              text-zinc-300
              resize-none
              outline-none
              focus:border-white/30
            "
          />

        </div>


        {/* RATIO */}

        <div className="mb-8">

          <p className="
            text-xs
            uppercase
            tracking-[0.3em]
            text-zinc-500
            mb-4
          ">
            Output Ratio
          </p>

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
              p-5
              outline-none
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

        <div className="mb-10">

          <p className="
            text-xs
            uppercase
            tracking-[0.3em]
            text-zinc-500
            mb-4
          ">
            Creative Direction
          </p>

          <select

            value={creativeStyle}

            onChange={(e) =>
              setCreativeStyle(
                e.target.value
              )
            }

            className="
              w-full
              rounded-[24px]
              bg-white/[0.04]
              border
              border-white/10
              p-5
              outline-none
            "
          >

            <option value="premium">
              Premium
            </option>

            <option value="cinematic">
              Cinematic
            </option>

            <option value="luxury">
              Luxury
            </option>

            <option value="minimal">
              Minimal
            </option>

          </select>

        </div>


        {/* GENERATE BUTTON */}

        <button

          onClick={generateAIWorkflow}

          disabled={loading}

          className="
            w-full
            py-7
            rounded-[30px]
            bg-white
            text-black
            text-2xl
            font-black
            hover:scale-[1.02]
            transition-all
            disabled:opacity-50
            mb-16
          "
        >

          {loading
            ? "Generating..."
            : "Generate AI Campaign"}

        </button>


        {/* TIMELINE */}

        <div>

          <p className="
            text-xs
            uppercase
            tracking-[0.3em]
            text-zinc-500
            mb-5
          ">
            Workflow Memory
          </p>

          <CreativeTimeline
            history={history}
          />

        </div>

      </div>


      {/* CENTER PANEL */}

      <div className="
        flex-1
        p-10
        overflow-y-auto
      ">

        <p className="
          text-xs
          uppercase
          tracking-[0.3em]
          text-zinc-500
          mb-5
        ">
          AI Workspace
        </p>

        <h2 className="
          text-6xl
          font-black
          mb-10
        ">
          Creative Directions
        </h2>


        <div className="
          w-full
          rounded-[40px]
          border
          border-white/10
          bg-[#050505]
          min-h-[760px]
          flex
          items-center
          justify-center
          overflow-hidden
          relative
        ">

          {generatedImage ? (

            <img

              src={generatedImage}

              alt="Generated Creative"

              className="
                w-full
                h-full
                object-contain
              "
            />

          ) : (

            <div className="text-center">

              <h3 className="
                text-5xl
                font-black
                mb-4
              ">
                Creative Workspace
              </h3>

              <p className="
                text-zinc-500
                text-xl
              ">
                Generate cinematic AI-powered
                campaign directions to begin.
              </p>

            </div>
          )}

        </div>

      </div>


      {/* RIGHT PANEL */}

      <div className="
        w-[420px]
        border-l
        border-white/10
        p-8
        overflow-y-auto
        bg-gradient-to-b
        from-black
        to-[#04101f]
      ">

        <ProductLibrary

          selectedProducts={
            selectedProducts
          }

          onSelect={
            toggleProduct
          }
        />

        <div className="mt-16">

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