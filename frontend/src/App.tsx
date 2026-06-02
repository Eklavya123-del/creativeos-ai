import {

  useState

} from "react"

import ProductLibrary from "./components/ProductLibrary"

import TemplateLibrary from "./components/TemplateLibrary"

import CreativeTimeline from "./components/CreativeTimeline"

import GenerationOverlay from "./components/GenerationOverlay"

import Login from "./pages/Login"

import Signup from "./pages/Signup"


const API_URL =
  import.meta.env.VITE_API_URL


interface TimelineItem {

  campaign: string

  result: string

  timestamp: string
}


function App() {

  // ============================================
  // AUTH
  // ============================================

  const [authenticated, setAuthenticated] =
    useState(

      localStorage.getItem(
        "admate-auth"
      ) === "true"
    )

  const [showSignup, setShowSignup] =
    useState(false)


  // ============================================
  // STATES
  // ============================================

  const [campaign, setCampaign] =
    useState("")

  const [ratio, setRatio] =
    useState("square")

  const [style, setStyle] =
    useState("premium")

  const [loading, setLoading] =
    useState(false)

  const [generatedImage, setGeneratedImage] =
    useState("")

  const [selectedProducts, setSelectedProducts] =
    useState<string[]>([])

  const [selectedTemplate, setSelectedTemplate] =
    useState<any>(null)

  const [history, setHistory] =
    useState<TimelineItem[]>([])


  // ============================================
  // AUTH GATE
  // ============================================

  if (!authenticated) {

    if (showSignup) {

      return (

        <Signup

          onSignup={() => {

            setShowSignup(false)
          }}

          onBack={() => {

            setShowSignup(false)
          }}
        />
      )
    }

    return (

      <Login

        onLogin={() => {

          localStorage.setItem(

            "admate-auth",

            "true"
          )

          setAuthenticated(true)
        }}

        onSignup={() => {

          setShowSignup(true)
        }}
      />
    )
  }


  // ============================================
  // PRODUCT SELECT
  // ============================================

  const toggleProduct = (

    product: string
  ) => {

    setSelectedProducts((prev) => {

      if (
        prev.includes(product)
      ) {

        return prev.filter(
          (p) => p !== product
        )
      }

      return [

        ...prev,

        product
      ]
    })
  }


  // ============================================
  // GENERATE
  // ============================================

  const generateAIWorkflow =
  async () => {

    try {

      if (
        selectedProducts.length === 0
      ) {

        alert(
          "Select product"
        )

        return
      }

      if (!selectedTemplate) {

        alert(
          "Select template"
        )

        return
      }

      setLoading(true)

      const formData =
        new FormData()

      formData.append(
        "campaign",
        campaign
      )

      formData.append(
        "ratio",
        ratio
      )

      formData.append(
        "style",
        style
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

      console.log(
        "SENDING:",
        {
          campaign,
          ratio,
          style,
          selectedProducts,
          selectedTemplate
        }
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

      console.log(
        "GENERATION RESPONSE:",
        data
      )

      if (
        data.status === "success"
      ) {

        setGeneratedImage(

          `${API_URL}${data.generated_image}`
        )

        setHistory((prev) => [

          {
            campaign,
            result:
              "Creative generated",

            timestamp:
              new Date().toLocaleString()
          },

          ...prev
        ])
      }

      else {

        alert(
          data.message ||
          "Generation failed"
        )
      }

    } catch (error) {

      console.error(error)

      alert(
        "Server error"
      )

    } finally {

      setLoading(false)
    }
  }

  // ============================================
  // UI
  // ============================================

  return (

    <div className="

      min-h-screen
      bg-[#050505]
      text-white
      overflow-hidden
    ">

      {/* OVERLAY */}

      {loading && (
        <GenerationOverlay />
      )}


      {/* MAIN */}

      <div className="
        flex
      ">

        {/* LEFT */}

        <div className="
          w-[420px]
          border-r
          border-white/10
          min-h-screen
          p-8
          overflow-y-auto
        ">

          <p className="
            text-zinc-500
            uppercase
            tracking-[0.3em]
            text-xs
            mb-3
          ">
            AdMate
          </p>

          <h1 className="
            text-5xl
            font-black
            leading-none
            mb-5
          ">
            AI Marketing
            Workspace
          </h1>

          <p className="
            text-zinc-500
            leading-relaxed
            mb-12
          ">
            Generate cinematic
            premium advertising
            creatives instantly.
          </p>

          <button

            onClick={() => {

              localStorage.removeItem(
                "admate-auth"
              )

              window.location.reload()
            }}

            className="
              text-zinc-500
              text-sm
              hover:text-white
              transition-all
              mb-12
            "
          >

            Logout

          </button>


          {/* CAMPAIGN */}

          <textarea

            placeholder="
            Describe your campaign...
            "

            value={campaign}

            onChange={(e) =>
              setCampaign(
                e.target.value
              )
            }

            className="
              w-full
              h-40
              bg-white/[0.04]
              border
              border-white/10
              rounded-[24px]
              p-5
              resize-none
              outline-none
              mb-8
            "
          />


          {/* RATIO */}

          <div className="
            mb-8
          ">

            <p className="
              text-zinc-500
              text-sm
              mb-3
            ">
              Ratio
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
                bg-white/[0.04]
                border
                border-white/10
                rounded-2xl
                px-5
                py-4
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

            <p className="
              text-zinc-500
              text-sm
              mb-3
            ">
              Style
            </p>

            <select

              value={style}

              onChange={(e) =>
                setStyle(
                  e.target.value
                )
              }

              className="
                w-full
                bg-white/[0.04]
                border
                border-white/10
                rounded-2xl
                px-5
                py-4
              "
            >

              <option value="premium">
                Premium
              </option>

              <option value="cinematic">
                Cinematic
              </option>

              <option value="modern">
                Modern
              </option>

            </select>

          </div>


          {/* BUTTON */}

          <button

            onClick={() => {

              if (

                !campaign ||

                selectedProducts.length === 0 ||

                !selectedTemplate
              ) {

                alert(
                  "Please select product, template and campaign"
                )

                return
              }

              generateAIWorkflow()
            }}

            className="
              w-full
              bg-white
              text-black
              py-5
              rounded-[24px]
              font-bold
              text-lg
            "
          >

            Generate Creative

          </button>

        </div>


        {/* CENTER */}

        <div className="
          flex-1
          p-8
          overflow-y-auto
        ">

          <div className="
            grid
            grid-cols-2
            gap-8
          ">

            <ProductLibrary

              selectedProducts={
                selectedProducts
              }

              onSelect={
                toggleProduct
              }
            />

            <TemplateLibrary

              ratio={ratio}

              selectedTemplate={
                selectedTemplate?.name || ""
              }

              onSelect={(template) =>
                setSelectedTemplate(
                  template
                )
              }
            />

          </div>


          {/* GENERATED */}

          {generatedImage && (

            <div className="
              mt-10
            ">

              <h2 className="
                text-3xl
                font-black
                mb-6
              ">
                Generated Creative
              </h2>

              <div className="
                rounded-[30px]
                overflow-hidden
                border
                border-white/10
              ">

                <img

                  src={generatedImage}

                  alt="Generated"

                  className="
                    w-full
                  "
                />

              </div>

            </div>
          )}

        </div>


        {/* RIGHT */}

        <div className="
          w-[400px]
          border-l
          border-white/10
          min-h-screen
          p-8
          overflow-y-auto
        ">

          <CreativeTimeline
            history={history}
          />

        </div>

      </div>

    </div>
  )
}

export default App