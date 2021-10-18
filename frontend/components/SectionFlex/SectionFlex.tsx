import styles from './SectionFlex.module.css';
import { SectionFlexProps } from './SectionFlex.props';
import cn from 'classnames';

export const SectionFlex = ({ block_style, children, className, ...props }: SectionFlexProps): JSX.Element => {    
    return (
        <section
            className={ cn(styles.section_flex, className, {
                [styles.section_flex]: block_style == 'section_flex', 
            })}
        >
            {children}
            
        </section>
    );
};