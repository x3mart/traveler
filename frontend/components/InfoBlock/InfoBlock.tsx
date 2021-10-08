import { InfoBlockProps } from "./InfoBlock.props";
import styles from './InfoBlock.module.css';
import cn from 'classnames';

export const InfoBlock = ({ border_color, height_block, children, ...props }: InfoBlockProps): JSX.Element => {
  return (
    <div
        className={ cn(styles.infoblock, className, {
            [styles.orange_left_border]: border_color == 'orange_left_border',
            [styles.blue_left_border]: border_color == 'blue_left_border',
            [styles.white_left_border]: border_color == 'white_left_border',
            [styles.travel_page]: height_block == 'travel_page',
        })}
        {...props}
    >  
        {children}
    </div>
  );
    
};

function className(InfoBlock: string, className: any, arg2: { [x: string]: boolean; }): string | undefined {
  throw new Error("Function not implemented.");
}
