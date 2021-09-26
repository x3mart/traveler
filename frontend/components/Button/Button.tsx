import styles from './Button.module.css';
import { ButtonProps } from './Button.props';
import ArrowIcon from '/public/polygon.svg';
import TravelerIcon from '/public/traveler.svg';
import cn from 'classnames';

export const Button = ({ appearance, arrow = 'none', traveler_suitcase = 'none', children, className, ...props }: ButtonProps): JSX.Element => {    
    return (
        <button
            className={ cn(styles.button, className, {
                [styles.primary]: appearance == 'primary',
                [styles.button_ghost]: appearance == 'button_ghost',
                [styles.ghost]: appearance == 'ghost',
                [styles.header_button]: appearance == 'header_button',
                [styles.header_button_travel]: appearance == 'header_button_travel',
                [styles.header_button_support]: appearance == 'header_button_support',
                [styles.header_button_country]: appearance == 'header_button_country',
                [styles.header_button_currency]: appearance == 'header_button_currency',
                [styles.header_button_liked]: appearance == 'header_button_liked',
                [styles.header_button_enter]: appearance == 'header_button_enter',
            })}
            {...props}
        >
            {traveler_suitcase !== 'none' && <span className={cn(styles.traveler_suitcase, {
            [styles.down]: traveler_suitcase == 'true'
            })}>
                <TravelerIcon />
            </span> }
            {children}
            {arrow !== 'none' && <span className={cn(styles.arrow, {
                [styles.down]: arrow == 'down'
            })}>
                <ArrowIcon className={styles.arr} {...props} />
            </span> }
            
        </button>
    );
};