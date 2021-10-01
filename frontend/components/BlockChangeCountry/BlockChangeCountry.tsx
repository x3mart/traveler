import styles from './BlockChangeCountry.module.css';
import { BlockChangeCountryProps } from './BlockChangeCountry.props';
import cn from 'classnames';
import { InfoBlock, Htag } from '..';
import EuropeIcon from '/public/europe.svg';
import AsiaIcon from '/public/asia.svg';
import AfricaIcon from '/public/africa.svg';
import SouthAmericaIcon from '/public/south-america.svg';
import AustraliaIcon from '/public/australia.svg';
import NorthAmericaIcon from '/public/north-america.svg';

export const BlockChangeCountry = ({ block_style, children, className, ...props }: BlockChangeCountryProps): JSX.Element => {     
    return (
        <div
            className={ cn(styles.block_viewed, className, {
                [styles.viewed_block]: block_style == 'viewed_block',
            })}
            {...props}
        >
            
            <div className={styles.wrapper} {...props}>
                {children}
                    <InfoBlock border_color='blue_left_border'>
                        <Htag tag='h2'>
                            Мир большой, сделайте первый шаг к его покорению 
                        </Htag>
                        <Htag tag='h4'>
                            Континенты и страны у твоих ног
                        </Htag>
                    </InfoBlock> 
                    <div className={styles.change_country_block}>
                        <div className={styles.change_country_block_item}>
                            <div className={styles.change_country_block_item_first_block}>
                                <EuropeIcon className={styles.europe_icon} />
                            </div>
                            <Htag tag='h4'>
                                Европа
                            </Htag>
                        </div>
                        <div className={styles.change_country_block_item}>
                            <div className={styles.change_country_block_item_first_block}>
                                <AsiaIcon className={styles.asia_icon} />
                            </div>
                            <Htag tag='h4'>
                                Азия
                            </Htag>
                        </div>
                        <div className={styles.change_country_block_item}>
                            <div className={styles.change_country_block_item_first_block}>
                                <AfricaIcon className={styles.africa_icon} />
                            </div>
                            <Htag tag='h4'>
                                Африка
                            </Htag>
                        </div>
                        <div className={styles.change_country_block_item}>
                            <div className={styles.change_country_block_item_first_block}>
                                <SouthAmericaIcon className={styles.south_america_icon} />
                            </div>
                            <Htag tag='h4'>
                                Северная Америка
                            </Htag>
                        </div>
                        <div className={styles.change_country_block_item}>
                            <div className={styles.change_country_block_item_first_block}>  
                                <AustraliaIcon className={styles.australia_icon} />
                            </div>
                            <Htag tag='h4'>
                                Австралия и Океания
                            </Htag>
                        </div>
                        <div className={styles.change_country_block_item}>
                            <div className={styles.change_country_block_item_first_block}>
                                <NorthAmericaIcon className={styles.north_america_icon} />
                            </div>
                            <Htag tag='h4'>
                                Северная Америка
                            </Htag>
                        </div>
                    </div>
                    
            </div> 
            
        </div>
    );
};