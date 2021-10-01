import styles from './BlockPresentation.module.css';
import { BlockPresentationProps } from './BlockPresentation.props';
import { Htag, Button, FormGetTour } from '../../components/';
import cn from 'classnames';

export const BlockPresentation = ({ block_style, children, className, ...props }: BlockPresentationProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.BlockPresentation, className, {
                [styles.presentation_block]: block_style == 'presentation_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                <Htag tag='h1'>traveler market - Маркетплейс авторских туров</Htag>
                <Button appearance='button_ghost'>Как это работает?</Button>
                <FormGetTour form_style='first_form_get_tour' children={undefined} />                   
            </div> 
            
        </div>
    );
};