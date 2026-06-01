import { useEffect, useState } from "react"

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

  const [uploading, setUploading] =
    useState(false)

  const API_URL =
    import.meta.env.VITE_API_URL


  // ============================================
  // FETCH TEMPLATES
  // ============================================

  const fetchTemplates =
    async () => {

      try {

        const response =
          await fetch(

            `${API_URL}/template-list/${ratio}`
          )

        const data =
          await response.json()

        setTemplates(
          data.templates || []
        )

      } catch (error) {

        console.error(error)
      }
    }


  useEffect(() => {

    fetchTemplates()

  }, [ratio])


  // ============================================
  // UPLOAD TEMPLATE
  // ============================================

  const uploadTemplate =
    async (
      e: React.ChangeEvent<HTMLInputElement>
    ) => {

      const file =
        e.target.files?.[0]

      if (!file) return

      try {

        setUploading(true)

        const formData =
          new FormData()

        formData.append(
          "file",
          file
        )

        formData.append(
          "ratio",
          ratio
        )

        await fetch(

          `${API_URL}/upload-template`,

          {
            method: "POST",

            body: formData
          }
        )

        await fetchTemplates()

      } catch (error) {

        console.error(error)

      } finally {

        setUploading(false)
      }
    }


  return (

    <div>

      {/* HEADER */}

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
            Layouts
          </p>

          <h2 className="
            text-3xl
            font-black
          ">
            Templates
          </h2>

        </div>

      </div>


      {/* UPLOAD BUTTON */}

      <label className="
        inline-flex
        items-center
        gap-3
        mb-8
        cursor-pointer
        rounded-[20px]
        bg-white
        text-black
        px-5
        py-3
        text-sm
        font-bold
        hover:scale-[1.02]
        transition-all
      ">

        <input

          type="file"

          accept=".png,.jpg,.jpeg,.webp"

          className="hidden"

          onChange={uploadTemplate}
        />

        {uploading
          ? "Uploading..."
          : "Upload Template"}

      </label>


      {/* GRID */}

      <div className="
        grid
        grid-cols-1
        gap-5
      ">

        {templates.map((template) => {

          const isSelected =
            selectedTemplate ===
            template.name

          return (

            <div

              key={template.name}

              onClick={() =>
                onSelect(
                  template.name
                )
              }

              className={`

                group
                cursor-pointer
                rounded-[28px]
                overflow-hidden
                border
                transition-all
                duration-300
                backdrop-blur-xl
                hover:scale-[1.02]
                bg-white/[0.04]

                ${
                  isSelected

                    ? "border-white shadow-[0_0_40px_rgba(255,255,255,0.15)]"

                    : "border-white/10"
                }

              `}
            >

              {/* IMAGE */}

              <div className="
                overflow-hidden
                bg-black
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

              <div className="p-5">

                <div className="
                  flex
                  items-center
                  justify-between
                ">

                  <div>

                    <p className="
                      text-sm
                      text-zinc-300
                      font-semibold
                      mb-1
                    ">
                      {template.name}
                    </p>

                    <p className="
                      text-xs
                      text-zinc-500
                    ">
                      {ratio} layout
                    </p>

                  </div>

                  {isSelected && (

                    <div className="
                      w-3
                      h-3
                      rounded-full
                      bg-white
                    " />

                  )}

                </div>

              </div>

            </div>
          )
        })}

      </div>

    </div>
  )
}

export default TemplateLibrary