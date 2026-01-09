function Modal({open, children}) {
  return (
    <div className={`fixed inset-0 flex justify-center items-center transition-colors ${open ? "visible bg-white/20" : "invisible"}`}>
        {/* Modal */}
        <div className={`p-6 w-1/2 bg-white rounded-xl shadow-2xl transition-all flex flex-col items-center ${open ? "scale-100 opacity-100" : "scale-125 opacity-0"}`}>
            {children}
        </div>
    </div>
  )
}

export default Modal