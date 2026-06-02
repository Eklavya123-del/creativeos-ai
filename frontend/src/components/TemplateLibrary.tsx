import {

  useEffect,
  useState

} from "react"

const API_URL =
  import.meta.env.VITE_API_URL

interface Props {

  ratio: string

  selectedTemplate: string

  onSelect: (
    template: string
  ) => void
}

function TemplateLibrary({

  ratio,

  selectedTemplate,

  onSelect

}: Props) {

  const [templates, setTemplates] =
    useState<string[]>([])

  // ============================================
  // FETCH TEMPLATES
  // ============================================

  useEffect(() => {

    const fetchTemplates =
      async () => {

        try {

          const response =
            await fetch(

              `${API_URL}/template-list/${ratio.toLowerCase()}`
            )

          const data =
            await response.json()

          console.log(
            "TEMPLATES:",
            data
          )

          setTemplates(
            data.templates || []
          )

        } catch (error) {

          console.error(
            "Template fetch error:",
            error
          )
        }
      }

    fetchTemplates()

  }, [ratio])

  return (

    <div>

      {/* HEADER */}

      <div className="
        mb-8
      ">

        <p className="
          text-zinc-500
          text-sm
          uppercase
          tracking-[0.2em]
          mb-2
        ">
          Layout System
        </p>

        <h2 className="
          text-3xl
          font-black
        ">
          Templates
        </h2>

      </div>


      {/* EMPTY */}

      {templates.length === 0 && (

        <div className="
          text-zinc-500
        ">
          No templates found.
        </div>
      )}


      {/* TEMPLATE GRID */}

      <div className="
        space-y-8
      ">

        {templates.map((template) => (

          <div

            key={template}

            onClick={() =>
              onSelect(template)
            }

            className={`
              relative
              rounded-[32px]
              overflow-hidden
              cursor-pointer
              border
              transition-all
              duration-300

              ${
                selectedTemplate === template

                  ? "border-white shadow-[0_0_40px_rgba(255,255,255,0.15)]"

                  : "border-white/10 hover:border-white/30"
              }
            `}
          >

            {/* TEMPLATE IMAGE */}

            <img

              src={`${API_URL}/templates/${ratio.toLowerCase()}/${template}`}

              alt={template}

              className="
                w-full
                h-[320px]
                object-cover
              "
            />

            {/* FOOTER */}

            <div className="
              absolute
              bottom-0
              left-0
              right-0
              bg-black/70
              backdrop-blur-xl
              p-5
            ">

              <p className="
                text-sm
                text-zinc-300
              ">
                {template}
              </p>

            </div>

          </div>
        ))}

      </div>

    </div>
  )
}

export default TemplateLibrary