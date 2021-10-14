import styles from './BlockCalendar.module.css';
import { BlockCalendarProps } from './BlockCalendar.props';
import cn from 'classnames';
import ArrowIconLeft from '/public/left_arrow.svg';
import ArrowIconRight from '/public/right_arrow.svg';


    


export const BlockCalendar = ({ children, className, ...props }: BlockCalendarProps): JSX.Element => {    
    return (
        <div
            className={ cn(styles.calendar, className, {
                
            })}
            {...props}
            
        >    
            {children}
            
            <div className={styles.calendar_block} {...props}>

                <div className={styles.calendar_block_month} {...props}>
                    <div className={styles.calendar_block_month_button} {...props}><ArrowIconLeft /></div>
                    <div className={styles.calendar_block_month_text} {...props}>Январь, 2021</div>
                    <div className={styles.calendar_block_month_button} {...props}><ArrowIconRight /></div>
                </div>
                <div className={styles.calendar_block_week} {...props}>
                    <div className={styles.calendar_block_week_day} {...props}>пн</div>
                    <div className={styles.calendar_block_week_day} {...props}>вт</div>
                    <div className={styles.calendar_block_week_day} {...props}>ср</div>
                    <div className={styles.calendar_block_week_day} {...props}>чт</div>
                    <div className={styles.calendar_block_week_day} {...props}>пт</div>
                    <div className={styles.calendar_block_week_day} {...props}>сб</div>
                    <div className={styles.calendar_block_week_day} {...props}>вс</div>
                </div>
                <div className={styles.calendar_block_days} {...props}>
                    <div className={styles.calendar_block_day} {...props}>29</div>
                    <div className={styles.calendar_block_day} {...props}>30</div>
                    <div className={styles.calendar_block_day} {...props}>1</div>
                    <div className={styles.calendar_block_day} {...props}>2</div>
                    <div className={styles.calendar_block_day} {...props}>3</div>
                    <div className={styles.calendar_block_day} {...props}>4</div>
                    <div className={styles.calendar_block_day} {...props}>5</div>
                    <div className={styles.calendar_block_day} {...props}>6</div>
                    <div className={styles.calendar_block_day} {...props}>7</div>
                    <div className={styles.calendar_block_day} {...props}>8</div>
                    <div className={styles.calendar_block_day} {...props}>9</div>
                    <div className={styles.calendar_block_day} {...props}>10</div>
                    <div className={styles.calendar_block_day} {...props}>11</div>
                    <div className={styles.calendar_block_day} {...props}>12</div>
                    <div className={styles.calendar_block_day} {...props}>13</div>
                    <div className={styles.calendar_block_day} {...props}>14</div>
                    <div className={styles.calendar_block_day} {...props}>15</div>
                    <div className={styles.calendar_block_day} {...props}>16</div>
                    <div className={styles.calendar_block_day} {...props}>17</div>
                    <div className={styles.calendar_block_day} {...props}>18</div>
                    <div className={styles.calendar_block_day} {...props}>19</div>
                    <div className={styles.calendar_block_day} {...props}>20</div>
                    <div className={styles.calendar_block_day} {...props}>21</div>
                    <div className={styles.calendar_block_day} {...props}>22</div>
                    <div className={styles.calendar_block_day} {...props}>23</div>
                    <div className={styles.calendar_block_day} {...props}>24</div>
                    <div className={styles.calendar_block_day} {...props}>25</div>
                    <div className={styles.calendar_block_day} {...props}>26</div>
                    <div className={styles.calendar_block_day} {...props}>27</div>
                    <div className={styles.calendar_block_day} {...props}>28</div>
                    <div className={styles.calendar_block_day} {...props}>29</div>
                    <div className={styles.calendar_block_day} {...props}>30</div>
                    <div className={styles.calendar_block_day} {...props}>1</div>
                    <div className={styles.calendar_block_day} {...props}>2</div>
                    <div className={styles.calendar_block_day} {...props}>3</div>
                </div>
                <div className={styles.calendar_block_submit} {...props}>Применить</div>
                <div className={styles.calendar_block_cancel} {...props}>Сбросить выбор</div>

            </div>
        </div>
    );
};