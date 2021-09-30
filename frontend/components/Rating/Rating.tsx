import { RatingProps } from "./Rating.props";
import styles from './Rating.module.css';
import cn from 'classnames';
import { Htag } from '..';

export const Rating = ({ border_color, children, ...props }: RatingProps): JSX.Element => {
  return (
    <div
        className={ cn(styles.rating, className, {
        })}
        {...props}
    >  
        {children}
        <Htag tag='h4'>5.0</Htag>
        <Htag tag='h3'>RATING</Htag>
    </div>
  );
    
};

function className(InfoBlock: string, className: any, arg2: { [x: string]: boolean; }): string | undefined {
  throw new Error("Function not implemented.");
}
