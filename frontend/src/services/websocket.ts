/**
 * WebSocket实时数据服务
 */

type MessageHandler = (data: any) => void;

class WebSocketService {
  private ws: WebSocket | null = null;
  private handlers: Map<string, Set<MessageHandler>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 3000;
  private subscribedStocks: Set<string> = new Set();

  /**
   * 连接WebSocket
   */
  connect(stockCode?: string): void {
    const baseUrl = `ws://${window.location.hostname}:8000`;
    const url = stockCode
      ? `${baseUrl}/ws/realtime/${stockCode}`
      : `${baseUrl}/ws/market`;

    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      console.log('WebSocket连接建立');
      this.reconnectAttempts = 0;

      // 如果是市场数据连接，重新订阅之前的股票
      if (!stockCode && this.subscribedStocks.size > 0) {
        this.subscribeStocks(Array.from(this.subscribedStocks));
      }
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        // 忽略心跳
        if (data.type === 'heartbeat') {
          return;
        }

        // 触发处理器
        const stockCode = data.code;
        if (stockCode && this.handlers.has(stockCode)) {
          this.handlers.get(stockCode)?.forEach(handler => handler(data));
        }

        // 触发全局处理器
        if (this.handlers.has('*')) {
          this.handlers.get('*')?.forEach(handler => handler(data));
        }
      } catch (error) {
        console.error('解析WebSocket消息失败:', error);
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket连接关闭');
      this.tryReconnect(stockCode);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket错误:', error);
    };
  }

  /**
   * 断开连接
   */
  disconnect(): void {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    this.subscribedStocks.clear();
  }

  /**
   * 尝试重连
   */
  private tryReconnect(stockCode?: string): void {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      setTimeout(() => this.connect(stockCode), this.reconnectDelay);
    }
  }

  /**
   * 订阅股票数据
   */
  subscribeStock(stockCode: string, handler: MessageHandler): void {
    // 添加处理器
    if (!this.handlers.has(stockCode)) {
      this.handlers.set(stockCode, new Set());
    }
    this.handlers.get(stockCode)!.add(handler);

    // 记录订阅
    this.subscribedStocks.add(stockCode);

    // 如果已连接，发送订阅消息
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        action: 'subscribe',
        stocks: [stockCode]
      }));
    }
  }

  /**
   * 批量订阅股票
   */
  subscribeStocks(stockCodes: string[]): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        action: 'subscribe',
        stocks: stockCodes
      }));
    }
    stockCodes.forEach(code => this.subscribedStocks.add(code));
  }

  /**
   * 取消订阅
   */
  unsubscribeStock(stockCode: string): void {
    this.handlers.delete(stockCode);
    this.subscribedStocks.delete(stockCode);

    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify({
        action: 'unsubscribe',
        stocks: [stockCode]
      }));
    }
  }

  /**
   * 添加全局处理器
   */
  onMessage(handler: MessageHandler): void {
    if (!this.handlers.has('*')) {
      this.handlers.set('*', new Set());
    }
    this.handlers.get('*')!.add(handler);
  }

  /**
   * 移除全局处理器
   */
  offMessage(handler: MessageHandler): void {
    this.handlers.get('*')?.delete(handler);
  }

  /**
   * 获取连接状态
   */
  get isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// 创建单例
export const wsService = new WebSocketService();
export default wsService;
