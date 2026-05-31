
import { useState } from "react"


interface Props {

  onLogin: () => void
}


function Login({

  onLogin

}: Props) {

  const [username, setUsername] =
    useState("")

  const [password, setPassword] =
    useState("")

  const [error, setError] =
    useState("")


  const handleLogin = () => {

    if (

      username === "Mohit Batra" &&
      password === "1"

    ) {

      onLogin()

    }

    else if (

      username === "Samriddhi" &&
      password === "HR"

    ) {

      onLogin()

    }

    else if (

      username === "Eklavya" &&
      password === "DEV"

    ) {

      onLogin()

    }

    else if (

      username === "Khushi" &&
      password === "Queen"

    ) {

      onLogin()

    }

    else {

      setError(
        "Invalid credentials"
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
      px-6
    ">

      <div className="
        w-full
        max-w-md
        bg-white/[0.04]
        border
        border-white/10
        backdrop-blur-2xl
        rounded-[40px]
        p-10
        shadow-2xl
      ">

        {/* LOGO */}
        <div className="
          mb-10
        ">

          <p className="
            text-zinc-500
            uppercase
            tracking-[0.3em]
            text-xs
            mb-4
          ">
            CreativeOS AI
          </p>

          <h1 className="
            text-5xl
            font-black
            leading-none
            mb-4
          ">
            Welcome
          </h1>

          <p className="
            text-zinc-400
            leading-relaxed
          ">
            AI-powered creative
            workflow operating system
            for modern wellness brands.
          </p>

        </div>


        {/* USERNAME */}
        <div className="
          mb-5
        ">

          <label className="
            text-sm
            text-zinc-500
            block
            mb-3
          ">
            Username
          </label>

          <input

            type="text"

            value={username}

            onChange={(e) =>
              setUsername(
                e.target.value
              )
            }

            className="
              w-full
              bg-black/40
              border
              border-white/10
              rounded-[20px]
              px-5
              py-4
              outline-none
              focus:border-white/30
              transition-all
            "

            placeholder="
              Enter username
            "
          />

        </div>


        {/* PASSWORD */}
        <div className="
          mb-8
        ">

          <label className="
            text-sm
            text-zinc-500
            block
            mb-3
          ">
            Password
          </label>

          <input

            type="password"

            value={password}

            onChange={(e) =>
              setPassword(
                e.target.value
              )
            }

            className="
              w-full
              bg-black/40
              border
              border-white/10
              rounded-[20px]
              px-5
              py-4
              outline-none
              focus:border-white/30
              transition-all
            "

            placeholder="
              Enter password
            "
          />

        </div>


        {/* ERROR */}
        {error && (

          <p className="
            text-red-400
            text-sm
            mb-5
          ">
            {error}
          </p>

        )}


        {/* BUTTON */}
        <button

          onClick={handleLogin}

          className="
            w-full
            bg-white
            text-black
            py-4
            rounded-[20px]
            font-black
            text-lg
            hover:scale-[1.02]
            transition-all
          "
        >

          Enter CreativeOS

        </button>

      </div>

    </div>
  )
}

export default Login

