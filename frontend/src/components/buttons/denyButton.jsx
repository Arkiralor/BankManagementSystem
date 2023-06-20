import './denyButton.css'

export default function DenyButton(props) {
    return (
        <button className="denyButton" onClick={props.onClick}>
            {props.text}
        </button>
    )
}