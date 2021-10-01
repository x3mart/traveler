import { SaleProps } from "./Sale.props";
import styles from './Sale.module.css';
import cn from 'classnames';
import { Htag } from '..';

export const Sale = ({ children, ...props }: SaleProps): JSX.Element => {
  return (
    <div
        className={ cn(styles.sale, className, {
        })}
        {...props}
    >  
        {children}
        <Htag tag='h4'>-50%</Htag>
        <Htag tag='h3'>SALE</Htag>
    </div>
  );
    
};

function className(InfoBlock: string, className: any, arg2: { [x: string]: boolean; }): string | undefined {
  throw new Error("Function not implemented.");
}
