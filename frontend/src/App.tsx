import {

  useEffect,
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
  // APP STATES
  // ============================================

  const [campaign, setCampaign] =
    useState("")

  const [selectedProducts, setSelectedProducts] =
    useState<string[]>([])

  const [selectedTemplate, setSelectedTemplate] =
    useState("")

  const [ratio, setRatio] =
    useState("square")

  const [style, setStyle] =
    useState("premium")

  const [loading, setLoading] =
    useState(false)

  const [generatedImage, setGeneratedImage] =
    useState("")

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
  // SELECT PRODUCT
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

  const generateAIWorkflow = async () => {

      try {

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

        if (
          data.status === "success"
        ) {

          const imageUrl =
            `${API_URL}${data.generated_image}`

          setGeneratedImage(
            imageUrl
          )

          setHistory((prev) => [

            {
              campaign,
              result:
                "Creative Generated",
              timestamp:
                new Date().toLocaleString()
            },

            ...prev
          ])
        }

        else {

          alert(
            data.message
          )
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

      {/* LOADING */}

      {loading && (

        <GenerationOverlay />
      )}


      {/* MAIN LAYOUT */}

      <div className="
        flex
      ">

        {/* SIDEBAR */}

        <div className="
          w-[420px]
          min-h-screen
          border-r
          border-white/10
          p-10
          overflow-y-auto
        ">

          {/* LOGO */}

          <div className="
            mb-14
          ">

            <p className="
              text-zinc-500
              text-sm
              uppercase
              tracking-[0.3em]
              mb-4
            ">
              AI Marketing Workspace
            </p>

            <h1 className="
              text-6xl
              font-black
              leading-none
              mb-8
            ">
              AdMate
            </h1>

            <p className="
              text-zinc-400
              leading-relaxed
              text-lg
              mb-6
            ">
              AI-powered marketing workspace
              for generating premium cinematic
              advertising creatives instantly.
            </p>

            {/* LOGOUT */}

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
              "
            >

              Logout

            </button>

          </div>


          {/* CAMPAIGN */}

          <div className="
            mb-10
          ">

            <p className="
              text-zinc-500
              text-sm
              uppercase
              tracking-[0.2em]
              mb-4
            ">
              Campaign Brief
            </p>

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
                bg-white/[0.04]
                border
                border-white/10
                rounded-[28px]
                p-6
                resize-none
                outline-none
                text-zinc-300
                backdrop-blur-xl
              "
            />

          </div>


          {/* RATIO */}

          <div className="
            mb-8
          ">

            <p className="
              text-zinc-500
              text-sm
              uppercase
              tracking-[0.2em]
              mb-4
            ">
              Format
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

          <div className="
            mb-10
          ">

            <p className="
              text-zinc-500
              text-sm
              uppercase
              tracking-[0.2em]
              mb-4
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
              py-5
              rounded-[24px]
              bg-white
              text-black
              font-black
              text-lg
              hover:scale-[1.02]
              transition-all
              duration-300
            "
          >

            Generate Creative

          </button>

        </div>


        {/* MAIN CONTENT */}

        <div className="
          flex-1
          p-10
          overflow-y-auto
        ">

          <div className="
            grid
            grid-cols-2
            gap-10
          ">

            {/* LEFT */}

            <div className="
              space-y-10
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
                  selectedTemplate
                }

                onSelect={
                  setSelectedTemplate
                }
              />

            </div>


            {/* RIGHT */}

            <div className="
              space-y-10
            ">

              {/* GENERATED IMAGE */}

              <div className="
                bg-white/[0.04]
                border
                border-white/10
                rounded-[32px]
                p-6
                backdrop-blur-xl
                overflow-hidden
              ">

                <div className="
                  flex
                  items-center
                  justify-between
                  mb-6
                ">

                  <div>

                    <p className="
                      text-zinc-500
                      text-sm
                      uppercase
                      tracking-[0.2em]
                      mb-2
                    ">
                      Output
                    </p>

                    <h2 className="
                      text-3xl
                      font-black
                    ">
                      Generated Creative
                    </h2>

                  </div>

                </div>


                <div className="
                  min-h-[600px]
                  rounded-[24px]
                  overflow-hidden
                  flex
                  items-center
                  justify-center
                  bg-black/40
                ">

                  {generatedImage ? (

                    <img

                      src={generatedImage}

                      alt="Generated"

                      className="
                        w-full
                        h-full
                        object-cover
                      "
                    />

                  ) : (

                    <p className="
                      text-zinc-500
                    ">
                      Generated creative
                      will appear here.
                    </p>

                  )}

                </div>

              </div>


              {/* TIMELINE */}

              <CreativeTimeline

                history={history}
              />

            </div>

          </div>

        </div>

      </div>

    </div>
  )
}

export default App