
import { useEffect, useState } from "react"


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

  const [uploading, setUploading] =
    useState(false)


  // -----------------------------------
  // UPLOAD TEMPLATE
  // -----------------------------------
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

          "http://127.0.0.1:8000/upload-template",

          {
            method: "POST",

            body: formData
          }
        )

        // REFRESH
        const response =
          await fetch(

            `http://127.0.0.1:8000/template-list/${ratio}`
          )

        const data =
          await response.json()

        setTemplates(
          data.templates || []
        )

      } catch (error) {

        console.error(error)

      } finally {

        setUploading(false)
      }
    }


  // -----------------------------------
  // FETCH TEMPLATES
  // -----------------------------------
  useEffect(() => {

    fetch(
      `http://127.0.0.1:8000/template-list/${ratio}`
    )

      .then((res) => res.json())

      .then((data) => {

        setTemplates(
          data.templates || []
        )
      })

      .catch((err) => {

        console.error(err)

        setTemplates([])
      })

  }, [ratio])


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
            Layout System
          </p>

          <h2 className="
            text-3xl
            font-black
          ">
            Templates
          </h2>

          {/* UPLOAD BUTTON */}
          <label className="
            inline-flex
            items-center
            gap-3
            mt-4
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

        </div>

      </div>


      {/* GRID */}
      <div className="
        grid
        grid-cols-2
        gap-4
      ">

        {templates.map((template) => {

          const isSelected =
            selectedTemplate ===
            template

          return (

            <div

              key={template}

              onClick={() =>
                onSelect(template)
              }

              className={`
                group
                cursor-pointer
                rounded-[28px]
                overflow-hidden
                border
                transition-all
                duration-300
                bg-white/[0.04]
                backdrop-blur-xl
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
                h-44
                overflow-hidden
                bg-[#181818]
              ">

                <img

                  src={`http://127.0.0.1:8000/templates/${ratio}/${template}`}

                  alt={template}

                  className="
                    w-full
                    h-full
                    object-cover
                    transition-all
                    duration-500
                    group-hover:scale-105
                  "
                />

              </div>


              {/* FOOTER */}
              <div className="
                p-5
              ">

                <div className="
                  flex
                  items-center
                  justify-between
                  mb-3
                ">

                  <p className="
                    text-sm
                    text-zinc-300
                    truncate
                  ">
                    {template}
                  </p>

                  {isSelected && (

                    <div className="
                      w-3
                      h-3
                      rounded-full
                      bg-white
                    " />

                  )}

                </div>

                <p className="
                  text-xs
                  text-zinc-500
                ">
                  Cinematic Layout
                </p>

              </div>

            </div>
          )
        })}

      </div>


      {/* EMPTY */}
      {templates.length === 0 && (

        <div className="
          mt-6
          text-zinc-500
          text-sm
        ">

          No templates found for
          this ratio.

        </div>
      )}

    </div>
  )
}

export default TemplateLibrary

