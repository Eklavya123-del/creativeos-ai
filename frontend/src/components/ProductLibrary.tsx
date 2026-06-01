
import { useEffect, useState } from "react"


interface Props {

  selectedProducts: string[]

  onSelect: (
    product: string
  ) => void
}


function ProductLibrary({

  selectedProducts,

  onSelect

}: Props) {

  const [products, setProducts] =
    useState<string[]>([])

  const [uploading, setUploading] =
    useState(false)
  const API_URL =
  import.meta.env.VITE_API_URL

  // -----------------------------------
  // UPLOAD PRODUCT
  // -----------------------------------
  const uploadProduct =
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

        await fetch(

          "${API_URL}/upload-product",

          {
            method: "POST",

            body: formData
          }
        )

        // REFRESH PRODUCTS
        const response =
          await fetch(
            "${API_URL}/products"
          )

        const data =
          await response.json()

        setProducts(
          data.products || []
        )

      } catch (error) {

        console.error(error)

      } finally {

        setUploading(false)
      }
    }


  // -----------------------------------
  // FETCH PRODUCTS
  // -----------------------------------
  useEffect(() => {

    fetch(
      "${API_URL}/products"
    )

      .then((res) => res.json())

      .then((data) => {

        setProducts(
          data.products || []
        )
      })

  }, [])


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
            Assets
          </p>

          <h2 className="
            text-3xl
            font-black
          ">
            Products
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

              onChange={uploadProduct}
            />

            {uploading
              ? "Uploading..."
              : "Upload Product"}

          </label>

        </div>

      </div>


      {/* GRID */}
      <div className="
        grid
        grid-cols-2
        gap-5
      ">

        {products.map((product) => {

          const isSelected =
            selectedProducts.includes(
              product
            )

          return (

            <div

              key={product}

              onClick={() =>
                onSelect(product)
              }

              className={`
                group
                cursor-pointer
                rounded-[30px]
                overflow-hidden
                border
                transition-all
                duration-300
                backdrop-blur-xl
                hover:scale-[1.03]
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
                h-52
                flex
                items-center
                justify-center
                bg-gradient-to-b
                from-[#181818]
                to-[#0b0b0b]
                overflow-hidden
              ">

                <img

                  src={`${API_URL}/uploads/products/${product}`}

                  alt={product}

                  className="
                    h-full
                    object-contain
                    transition-all
                    duration-500
                    group-hover:scale-110
                  "
                />

              </div>


              {/* FOOTER */}
              <div className="
                p-5
              ">

                <p className="
                  text-sm
                  text-zinc-300
                  truncate
                  mb-2
                ">
                  {product}
                </p>

                <div className="
                  flex
                  items-center
                  justify-between
                ">

                  <p className="
                    text-xs
                    text-zinc-500
                  ">
                    Wellness Product
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

              </div>

            </div>
          )
        })}

      </div>

    </div>
  )
}

export default ProductLibrary

