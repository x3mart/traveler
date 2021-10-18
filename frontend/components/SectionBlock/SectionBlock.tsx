import styles from './SectionBlock.module.css';
import { SectionBlockProps } from './SectionBlock.props';
import cn from 'classnames';

export const SectionBlock = ({ block_style, children, className }: SectionBlockProps): JSX.Element => {    
    return (
        <section
            className={ cn(styles.section_flex, className, {
                [styles.section_block]: block_style == 'section_block',
            })}
        >
            {children}
            
        </section>
    );
};