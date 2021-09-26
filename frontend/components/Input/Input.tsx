import styles from './Input.module.css';
import { InputProps } from './Input.props';
import cn from 'classnames';

export const Input = ({ className, choice, ...props }: InputProps): JSX.Element => {    
    return (
        <input className={cn(className, styles.input, {
            [styles.place]: choice == 'place',
            [styles.calendar]: choice == 'calendar',
        })} {...props}/>
    );
};