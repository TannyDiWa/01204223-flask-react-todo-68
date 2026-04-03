import { render, screen } from '@testing-library/react'
import { vi } from 'vitest'
import App from '../App.jsx'

const mockResponse = (body, ok = true) => Promise.resolve({
  ok,
  json: () => Promise.resolve(body),
});

const todoItem1 = { id: 1, title: 'First todo', done: false, comments: [] };
const todoItem2 = { id: 2, title: 'Second todo', done: false, comments: [
  { id: 1, message: 'First comment' },
  { id: 2, message: 'Second comment' },
] };
const originalTodoList = [ todoItem1, todoItem2 ];

describe('App', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  afterEach(() => {
    vi.resetAllMocks();
    vi.unstubAllGlobals();
  });

  it('renders correctly', async () => {
    global.fetch.mockImplementationOnce(() => mockResponse(originalTodoList));

    render(<App />);

    expect(await screen.findByText('First todo')).toBeInTheDocument();
    expect(await screen.findByText('Second todo')).toBeInTheDocument();
    expect(await screen.findByText('First comment')).toBeInTheDocument();
    expect(await screen.findByText('Second comment')).toBeInTheDocument();
  });

  it('toggles done on a todo item', async() => {
    // เตรียมค่าสำหรับคืนหลังกด toggle done แล้ว
    const toggledTodoItem1 = { ...todoItem1, done: true };
    // mock fetch
    global.fetch
      .mockImplementationOnce(() => mockResponse(originalTodoList))
      .mockImplementationOnce(() => mockResponse(toggledTodoItem1));

    render(<App />);

    // assert ก่อนว่าของเดิม todo item แรกไม่ได้มีคลาส done
    expect(await screen.findByText('First todo')).not.toHaveClass('done');

    // หาปุ่ม จะเจอ 2 ปุ่ม (เพราะว่ามี 2 todo item)
    const toggleButtons = await screen.findAllByRole('button', { name: /toggle/i })
    // เลือกกดปุ่มแรก
    toggleButtons[0].click();

    // ตรวจสอบว่า todo item นั้นเปลี่ยนคลาสเป็น done แล้ว
    expect(await screen.findByText('First todo')).toHaveClass('done');
    
    // ตรวจสอบ URL
    expect(global.fetch).toHaveBeenLastCalledWith(expect.stringMatching(/1\/toggle/), { method: 'PATCH' });
  });
});
