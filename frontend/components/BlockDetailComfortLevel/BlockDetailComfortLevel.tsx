import styles from './BlockDetailComfortLevel.module.css';
import { BlockDetailComfortLevelProps } from './BlockDetailComfortLevel.props';
import cn from 'classnames';
import { Htag } from '..';
import StarIconBig from '/public/greenstarbig.svg';
import FlagIconBig from '/public/FlagBig.svg';

export const BlockDetailComfortLevel = ({ block_style, children, className, ...props }: BlockDetailComfortLevelProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <div className={styles.comfort_block} {...props}>
                        <div className={styles.comfort_block_item} {...props}>
                            <Htag tag='h3'>
                                3 
                            </Htag>
                            <Htag tag='h4'>
                                Комфорт
                            </Htag>
                        </div>
                        <div className={styles.comfort_block_item} {...props}>
                            <div className={styles.comfort_block_item_level} {...props}>
                                <div className={styles.comfort_block_item_level_round} {...props}></div>
                                <div className={styles.comfort_block_item_level_round} {...props}></div>
                                <div className={styles.comfort_block_item_level_round} {...props}></div>
                                <div className={styles.comfort_block_item_level_round} {...props}></div>
                                <div className={styles.comfort_block_item_level_round} {...props}></div>
                            </div>
                            <Htag tag='h4'>
                                Сложность
                            </Htag>
                        </div>
                        <div className={styles.comfort_block_item} {...props}>
                            <FlagIconBig />
                            <Htag tag='h4'>
                                Язык
                            </Htag>
                        </div>
                        <div className={styles.comfort_block_item} {...props}>
                            <Htag tag='h3'>
                                18 - 35
                            </Htag>
                            <Htag tag='h4'>
                                Средний возраст
                            </Htag>
                        </div>
                    </div>                    
            </div> 
            
        </div>
    );
};