import { useState } from "react"

const API_URL =
  import.meta.env.VITE_API_URL

interface Props {

  onSignup: () => void

  onBack: () => void
}

function Signup({

  onSignup,

  onBack

}: Props) {

  const [username, setUsername] =
    useState("")

  const [email, setEmail] =
    useState("")

  const [password, setPassword] =
    useState("")

  // ============================================
  // SIGNUP
  // ============================================

  const signup = async () => {

    try {

      const response = await fetch(

        `${API_URL}/signup`,

        {
          method: "POST",

          headers: {

            "Content-Type":
              "application/json"
          },

          body: JSON.stringify({

            username,
            email,
            password
          })
        }
      )

      const data =
        await response.json()

      if (
        response.ok
      ) {

        alert(
          "Signup successful"
        )

        onSignup()
      }

      else {

        alert(
          data.detail ||
          data.message ||
          "Signup failed"
        )
      }

    } catch (error) {

      console.error(error)

      alert(
        "Server error"
      )
    }
  }

  return (

    <div className="
      min-h-screen
      bg-black
      text-white
      flex
      items-center
      justify-center
    ">

      <div className="
        w-[420px]
        bg-zinc-900
        border
        border-white/10
        rounded-[32px]
        p-10
      ">

        <button

          onClick={onBack}

          className="
            text-zinc-500
            mb-8
            hover:text-white
            transition-all
          "
        >

          ← Back

        </button>

        <h1 className="
          text-4xl
          font-black
          mb-10
        ">
          Create Account
        </h1>

        <div className="
          space-y-5
        ">

          <input

            placeholder="Username"

            value={username}

            onChange={(e) =>
              setUsername(
                e.target.value
              )
            }

            className="
              w-full
              bg-zinc-800
              border
              border-white/10
              rounded-2xl
              px-5
              py-4
            "
          />

          <input

            placeholder="Email"

            value={email}

            onChange={(e) =>
              setEmail(
                e.target.value
              )
            }

            className="
              w-full
              bg-zinc-800
              border
              border-white/10
              rounded-2xl
              px-5
              py-4
            "
          />

          <input

            type="password"

            placeholder="Password"

            value={password}

            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }

            className="
              w-full
              bg-zinc-800
              border
              border-white/10
              rounded-2xl
              px-5
              py-4
            "
          />

          <button

            onClick={signup}

            className="
              w-full
              bg-white
              text-black
              py-4
              rounded-2xl
              font-bold
            "
          >

            Sign Up

          </button>

        </div>

      </div>

    </div>
  )
}

export default Signup