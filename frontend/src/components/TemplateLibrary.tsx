import {
  useEffect,
  useState
} from "react"

const API_URL =
  import.meta.env.VITE_API_URL

interface Template {

  name: string

  image: string
}

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
    useState<Template[]>([])

  useEffect(() => {

    fetch(
      `${API_URL}/template-list/${ratio}`
    )

      .then((res) => res.json())

      .then((data) => {

        setTemplates(
          data.templates || []
        )
      })

      .catch((err) => {

        console.error(err)
      })

  }, [ratio])

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
          bg-white/[0.04]
          border
          border-white/10
          rounded-[24px]
          p-6
        ">

          <p className="
            text-zinc-500
          ">
            No templates found
          </p>

        </div>
      )}

      {/* GRID */}

      <div className="
        space-y-5
      ">

        {templates.map((template) => {

          const isSelected =
            selectedTemplate === template.name

          return (

            <div

              key={template.name}

              onClick={() =>
                onSelect(template.name)
              }

              className={`
                group
                cursor-pointer
                overflow-hidden
                rounded-[30px]
                border
                transition-all
                duration-300
                bg-white/[0.04]
                hover:scale-[1.02]

                ${
                  isSelected

                    ? "border-white shadow-[0_0_40px_rgba(255,255,255,0.15)]"

                    : "border-white/10"
                }
              `}
            >

              {/* IMAGE */}

              <div className="
                relative
                overflow-hidden
              ">

                <img

                  src={`${API_URL}${template.image}`}

                  alt={template.name}

                  className="
                    w-full
                    h-[260px]
                    object-cover
                    transition-all
                    duration-500
                    group-hover:scale-105
                  "
                />

              </div>

              {/* FOOTER */}

              <div className="
                p-4
              ">

                <p className="
                  text-sm
                  text-zinc-300
                  truncate
                ">
                  {template.name}
                </p>

              </div>

            </div>
          )
        })}

      </div>

    </div>
  )
}

export default TemplateLibrary