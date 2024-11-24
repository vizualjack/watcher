const fs = require('fs');


export enum LogLevel {
    DEBUG,
    INFO,
    WARNING,
    ERROR,
}


export class Logger {
    logLevel: LogLevel;
    logFilePath: string|undefined;

    constructor(logLevel: LogLevel, logFilePath: string|undefined = undefined) {
        this.logLevel = logLevel;
        this.logFilePath = logFilePath;
    }

    debug(message: string) {
        this.#log(LogLevel.DEBUG, message);
    }

    info(message: string) {
        this.#log(LogLevel.INFO, message);
    }

    warning(message: string) {
        this.#log(LogLevel.WARNING, message);
    }

    error(message: string) {
        this.#log(LogLevel.ERROR, message);
    }

    #log(level: LogLevel, message: string) {
        if (level >= this.logLevel) {
            this.#printLine(level, message);
        }
    }

    #printLine(level: LogLevel, message: string) {
        const logMessage = `[${this.#getLocalTimestamp()}] [${LogLevel[level]}] ${message}`;
        console.log(logMessage);
        if (this.logFilePath) fs.appendFileSync(this.logFilePath, logMessage + "\n");
    }

    #getLocalTimestamp() {
        const now = new Date();
        const options: Intl.DateTimeFormatOptions = {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false,
        };
        return new Intl.DateTimeFormat("de-DE", options).format(now);
    }
}

require('dotenv').config(); // Load .env file
export let logLevel = LogLevel[process.env.LOG_LEVEL?.toUpperCase() as keyof typeof LogLevel];
if(logLevel == undefined) LogLevel.ERROR;
export const logger = new Logger(
    logLevel,
    process.env.LOG_FILE_PATH
);