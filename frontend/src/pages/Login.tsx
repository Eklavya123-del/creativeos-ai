import {

  useState

} from "react"

import loginImage from "../assets/login.png"

import ForgotPasswordPopup from "../components/ForgotPasswordPopup"

const API_URL =
  import.meta.env.VITE_API_URL

interface Props {

  onLogin: () => void

  onSignup: () => void
}

function Login({

  onLogin,

  onSignup

}: Props) {

  const [email, setEmail] =
    useState("")

  const [password, setPassword] =
    useState("")

  const [failedAttempts, setFailedAttempts] =
    useState(0)

  const [showForgot, setShowForgot] =
    useState(false)

  const handleLogin = async () => {

  try {

    const response = await fetch(

      `${API_URL}/login`,

      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json"
        },

        body: JSON.stringify({

  username: email,
  password
})
      }
    )

    const data =
      await response.json()

    if (!response.ok) {

      setFailedAttempts(
        (prev) => prev + 1
      )

      alert(

        data.detail ||

        data.message ||

        "Invalid credentials"
      )

      return
    }

    alert(
      data.message
    )

    onLogin()

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
      flex
      bg-white
    ">

      {/* LEFT */}

      <div className="
        w-1/2
        flex
        items-center
        justify-center
      ">

        <div className="
          w-[420px]
        ">

          <p className="
            text-zinc-500
            mb-3
          ">
            Start your journey
          </p>

          <h1 className="
            text-5xl
            font-black
            mb-12
          ">
            Welcome to AdMate
          </h1>

          <div className="
            space-y-6
          ">

            <input

              placeholder="E-mail"

              value={email}

              onChange={(e) =>
                setEmail(
                  e.target.value
                )
              }

              className="
                w-full
                border
                rounded-2xl
                px-5
                py-5
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
                border
                rounded-2xl
                px-5
                py-5
              "
            />

            <button

              onClick={handleLogin}

              className="
                w-full
                bg-blue-500
                text-white
                py-5
                rounded-2xl
                font-bold
              "
            >
              Login
            </button>
            <button

            onClick={onSignup}

            className="
              text-blue-500
              font-medium
              mt-5
            "
          >

            Create Account

          </button>
            {failedAttempts >= 2 && (

              <button

                onClick={() =>
                  setShowForgot(true)
                }

                className="
                  text-blue-500
                  font-medium
                "
              >
                Forgot credentials?
              </button>
            )}

          </div>

        </div>

      </div>


      {/* RIGHT */}

      <div className="
        w-1/2
        h-screen
      ">

        <img

          src={loginImage}

          alt="Login"

          className="
            w-full
            h-full
            object-cover
          "
        />

      </div>


      {showForgot && (

        <ForgotPasswordPopup

          onClose={() => {

            localStorage.setItem(
              "admate-auth",
              "true"
            )

            onLogin()
          }}
        />
      )}

    </div>
  )
}

export default Login