import './affirmativeButton.css'


export default function AffirmativeButton(props) {
    return (
        <button className="affirmativeButton" onClick={props.onClick}>
            {props.text}
        </button>
    )
}