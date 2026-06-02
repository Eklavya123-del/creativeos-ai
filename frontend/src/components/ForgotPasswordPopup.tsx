interface Props {

  onClose: () => void
}

function ForgotPasswordPopup({

  onClose

}: Props) {

  return (

    <div className="
      fixed
      inset-0
      bg-black/70
      backdrop-blur-xl
      flex
      items-center
      justify-center
      z-[999]
    ">

      <div className="
        bg-zinc-900
        border
        border-white/10
        rounded-[32px]
        p-10
        max-w-md
        text-center
      ">

        <div className="
          text-6xl
          mb-6
        ">
          🤔
        </div>

        <h2 className="
          text-3xl
          font-black
          mb-4
        ">
          Access Granted
        </h2>

        <p className="
          text-zinc-400
          leading-relaxed
          mb-8
        ">
          Itna smart insaan intruder toh nhi ho sakta...
          <br />
          Jao access diya 😭✨
        </p>

        <button

          onClick={onClose}

          className="
            bg-white
            text-black
            px-8
            py-4
            rounded-2xl
            font-bold
          "
        >
          Continue
        </button>

      </div>

    </div>
  )
}

export default ForgotPasswordPopup