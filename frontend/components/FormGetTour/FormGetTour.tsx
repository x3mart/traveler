import styles from './FormGetTour.module.css';
import { FormGetTourProps } from './FormGetTour.props';
import { Input, Button } from '../../components';
import MagnifierIcon from '/public/magnifier.svg';
import cn from 'classnames';

export const FormGetTour = ({ form_style, className, children, ...props }: FormGetTourProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.FormGetTour, className, {
                [styles.first_form_get_tour]: form_style == 'first_form_get_tour',
                [styles.second_form_get_tour]: form_style == 'second_form_get_tour'
            })}
            {...props}
        >
            {children}
            <Input choice="place" placeholder="Страна, регион или город" />
            <Input choice="calendar" placeholder="Выберите даты" />
            <Button appearance='primary'><MagnifierIcon />Подобрать тур</Button>  
        </div>
    );
};