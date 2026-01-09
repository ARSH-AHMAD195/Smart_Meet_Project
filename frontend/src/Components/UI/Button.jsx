function Button({children, className}) {

    const classes = `${className}`;
    const renderButton = () =>(
        <button className={classes}>
            {children}
        </button>
    )
    return renderButton();
}

export default Button